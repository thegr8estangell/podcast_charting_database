"""
daily_scrape.py — entry point for the daily GitHub Action.

Apple (podcast-intelligence) + Spotify (more-podcast-intelligence) only —
YouTube dropped per request. Every chart entry is tagged with is_iheart
using the full identifier list in iheart_identifiers.py.

NOTE: reconstructed from the working code in our past chats. Double
check secret names, selectors, and the Spotify approach still match
your current repo state before trusting this in production.
"""

import os
import re
import time
from datetime import datetime, timezone

import requests
from playwright.sync_api import sync_playwright

from db import get_conn, upsert_show, record_chart_entry
from iheart_identifiers import check_iheart

TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")


# =====================================================
# APPLE  (from podcast-intelligence)
# =====================================================

def scrape_apple_charts() -> list[dict]:
    """Top Shows + New Shows + New & Noteworthy (RSS) + Editors Pick (Playwright)."""
    out = []

    apple_feeds = [
        # Apple deprecated rss.itunes.apple.com — new_shows and
        # new_and_noteworthy used to live there but now return empty
        # responses. Top Series + Editors Pick (scraped below via
        # Playwright) are the best available substitute for curated/
        # emerging show coverage.
        ("https://itunes.apple.com/us/rss/toppodcasts/limit=25/json", "top25"),
    ]

    for feed_url, chart_type in apple_feeds:
        try:
            r = requests.get(feed_url, timeout=15)
            data = r.json()
            entries = data.get("feed", {}).get("entry", [])
            for i, entry in enumerate(entries, start=1):
                apple_id = entry.get("id", {}).get("attributes", {}).get("im:id", "")
                title = entry.get("im:name", {}).get("label", "")
                author = entry.get("im:artist", {}).get("label", "")
                out.append({
                    "show_id": f"apple:{apple_id}" if apple_id else f"apple:{title.lower()}",
                    "name": title,
                    "chart_type": chart_type,
                    "rank": i,
                    "feed_url": None,
                    "is_iheart": check_iheart(title, author),
                })
            print(f"  Apple {chart_type}: {len(entries)} entries")
        except Exception as e:
            print(f"  Apple {chart_type} failed: {e}")

    # Editors Pick carousel (Playwright — page structure can drift)
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("https://podcasts.apple.com/us/browse", wait_until="networkidle", timeout=30000)
            page.wait_for_selector("[data-testid='shelf-item-list']", timeout=15000)
            cards = page.query_selector_all("[data-testid='shelf-item-list'] .editorial-card")
            for i, card in enumerate(cards, start=1):
                link = card.query_selector("[data-testid='hero-lockup__link']")
                title_el = card.query_selector("[data-testid='hero-lockup__title']")
                title = title_el.inner_text() if title_el else ""
                url = link.get_attribute("href") if link else ""
                m = re.search(r"id(\d+)", url or "")
                apple_id = m.group(1) if m else None
                out.append({
                    "show_id": f"apple:{apple_id}" if apple_id else f"apple:{title.lower()}",
                    "name": title,
                    "chart_type": "editors_pick",
                    "rank": i,
                    "feed_url": None,
                    "is_iheart": check_iheart(title),
                })
            browser.close()
            print(f"  Apple editors_pick: {len(cards)} entries")
    except Exception as e:
        print(f"  Apple editors_pick failed: {e}")

    # Top Series (Playwright — scrolls the shelf to load up to 25, not just
    # the ~7 that render before scrolling)
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("https://podcasts.apple.com/us/charts", wait_until="networkidle", timeout=30000)
            page.wait_for_selector("[aria-label='Top Series']", timeout=15000)

            # Scroll the Top Series shelf via its Next arrow until 25 items
            # have loaded or the shelf is exhausted
            for _ in range(15):
                items = page.query_selector_all(
                    "[aria-label='Top Series'] [data-testid='shelf-item-list'] > *"
                )
                if len(items) >= 25:
                    break
                next_btn = page.query_selector("[aria-label='Top Series'] [data-testid='shelf-button-right']")
                if not next_btn:
                    break
                if next_btn.get_attribute("disabled") is not None:
                    break
                next_btn.click()
                page.wait_for_timeout(800)

            items = page.query_selector_all(
                "[aria-label='Top Series'] [data-testid='shelf-item-list'] > *"
            )[:25]

            for i, item in enumerate(items, start=1):
                title_el = item.query_selector("[data-testid='product-lockup-title']")
                author_el = item.query_selector("[data-testid='product-lockup-subtitle']")
                link_el = item.query_selector("a")
                title = title_el.inner_text().strip() if title_el else ""
                author = author_el.inner_text().strip() if author_el else ""
                url = link_el.get_attribute("href") if link_el else ""
                m = re.search(r"id(\d+)", url or "")
                apple_id = m.group(1) if m else None
                out.append({
                    "show_id": f"apple:{apple_id}" if apple_id else f"apple:{title.lower()}",
                    "name": title,
                    "chart_type": "top_series",
                    "rank": i,
                    "feed_url": None,
                    "is_iheart": check_iheart(title, author),
                })
            browser.close()
            print(f"  Apple top_series: {len(items)} entries")
    except Exception as e:
        print(f"  Apple top_series failed: {e}")

    return out


# =====================================================
# SPOTIFY  (from more-podcast-intelligence)
# =====================================================

def get_spotify_token() -> str:
    client_id = os.environ["SPOTIFY_CLIENT_ID"]
    client_secret = os.environ["SPOTIFY_CLIENT_SECRET"]
    r = requests.post(
        "https://accounts.spotify.com/api/token",
        data={"grant_type": "client_credentials"},
        auth=(client_id, client_secret),
        timeout=15,
    )
    r.raise_for_status()
    return r.json()["access_token"]


def _spotify_show_id_from_url(url: str) -> str | None:
    m = re.search(r"show/([A-Za-z0-9]+)", url or "")
    return m.group(1) if m else None


def scrape_spotify_charts() -> list[dict]:
    """
    NOTE: Spotify's API has no direct 'top charts' endpoint -- this queries
    top shows per category as a proxy for 'top_shows', plus an
    'editors_pick' pass via editorial search terms. If you've since
    switched to scraping podcastcharts.byspotify.com directly (the other
    approach explored in that chat), swap this function body for that
    version instead -- it'll give you real chart ranks rather than a
    search-based proxy.
    """
    out = []
    try:
        token = get_spotify_token()
        headers = {"Authorization": f"Bearer {token}"}

        # --- Top Shows proxy (category search) ---
        categories = ["true crime", "news", "comedy", "society", "business"]
        seen = set()
        rank = 0
        for query in categories:
            r = requests.get(
                "https://api.spotify.com/v1/search",
                headers=headers,
                params={"q": query, "type": "show", "market": "US", "limit": 3},
                timeout=15,
            )
            if r.status_code != 200:
                continue
            for show in r.json().get("shows", {}).get("items", []):
                if not show or show.get("name") in seen:
                    continue
                seen.add(show.get("name"))
                rank += 1
                url = show.get("external_urls", {}).get("spotify", "")
                title = show.get("name", "")
                author = show.get("publisher", "")
                out.append({
                    "show_id": f"spotify:{_spotify_show_id_from_url(url) or title.lower()}",
                    "name": title,
                    "chart_type": "top_shows",
                    "rank": rank,
                    "feed_url": url,
                    "is_iheart": check_iheart(title, author),
                })
            time.sleep(0.3)
        print(f"  Spotify top_shows: {len(out)} entries")

        # --- Editors Pick proxy (editorial search terms) ---
        editorial_queries = ["editors pick podcast", "best new podcast", "featured podcast spotlight"]
        seen_ep = set()
        ep_rank = 0
        for query in editorial_queries:
            r = requests.get(
                "https://api.spotify.com/v1/search",
                headers=headers,
                params={"q": query, "type": "show", "market": "US", "limit": 4},
                timeout=15,
            )
            if r.status_code != 200:
                continue
            for show in r.json().get("shows", {}).get("items", []):
                if not show or show.get("name") in seen_ep or show.get("name") in seen:
                    continue
                seen_ep.add(show.get("name"))
                ep_rank += 1
                url = show.get("external_urls", {}).get("spotify", "")
                title = show.get("name", "")
                author = show.get("publisher", "")
                out.append({
                    "show_id": f"spotify:{_spotify_show_id_from_url(url) or title.lower()}",
                    "name": title,
                    "chart_type": "editors_pick",
                    "rank": ep_rank,
                    "feed_url": url,
                    "is_iheart": check_iheart(title, author),
                })
            time.sleep(0.3)
        print(f"  Spotify editors_pick: {len(seen_ep)} entries")

    except Exception as e:
        print(f"  Spotify failed: {e}")

    return out


# =====================================================
# STORE + MAIN
# =====================================================

def store_results(conn, platform: str, results: list[dict]):
    for r in results:
        upsert_show(conn, show_id=r["show_id"], platform=platform,
                    name=r["name"], feed_url=r.get("feed_url"), seen_date=TODAY)
        record_chart_entry(conn, show_id=r["show_id"], platform=platform,
                            chart_type=r["chart_type"], rank=r["rank"],
                            snapshot_date=TODAY, is_iheart=r.get("is_iheart", False))


def main():
    conn = get_conn("chart_history.db")

    apple_results = scrape_apple_charts()
    store_results(conn, "apple", apple_results)

    spotify_results = scrape_spotify_charts()
    store_results(conn, "spotify", spotify_results)

    conn.commit()

    all_results = apple_results + spotify_results
    iheart_hits = [r for r in all_results if r.get("is_iheart")]
    print(f"\n{TODAY}: {len(all_results)} chart entries stored, {len(iheart_hits)} iHeart matches")
    if iheart_hits:
        for r in iheart_hits:
            print(f"   -> {r['name']}")

    conn.close()


if __name__ == "__main__":
    main()
