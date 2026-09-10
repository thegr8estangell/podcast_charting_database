"""
db.py — SQLite helper for chart + video history.

Drop this in your more-podcast-intelligence repo alongside the scraper.
The .db file gets committed to git just like your CSVs are today —
same workflow (git stash / pull --rebase / stash pop / push), just a
different file being modified.

Usage from your scraper:

    from db import get_conn, upsert_show, record_chart_entry, record_video_status

    conn = get_conn("chart_history.db")
    upsert_show(conn, show_id="spotify:show:abc123", platform="spotify",
                name="Some Podcast", feed_url=None, seen_date="2026-09-08")
    record_chart_entry(conn, show_id="spotify:show:abc123", platform="spotify",
                        chart_type="top25", rank=14, snapshot_date="2026-09-08")
    record_video_status(conn, show_id="spotify:show:abc123",
                         checked_date="2026-09-08", has_video=False, video_url=None)
    conn.commit()
    conn.close()
"""

import sqlite3
from pathlib import Path

SCHEMA_PATH = Path(__file__).parent / "schema.sql"


def get_conn(db_path: str = "chart_history.db") -> sqlite3.Connection:
    """Open (and initialize if needed) the chart history database."""
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")
    with open(SCHEMA_PATH, "r") as f:
        conn.executescript(f.read())
    return conn


def upsert_show(conn, show_id: str, platform: str, name: str,
                 feed_url: str | None, seen_date: str):
    """Insert a show if new; do nothing if it already exists (keeps first_seen intact)."""
    conn.execute(
        """
        INSERT INTO shows (show_id, platform, name, feed_url, first_seen)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(show_id) DO NOTHING
        """,
        (show_id, platform, name, feed_url, seen_date),
    )


def record_chart_entry(conn, show_id: str, platform: str, chart_type: str,
                        rank: int, snapshot_date: str, is_iheart: bool = False):
    """Record one show's rank on one chart on one day. Safe to re-run (upserts on conflict)."""
    conn.execute(
        """
        INSERT INTO chart_entries (show_id, platform, chart_type, rank, snapshot_date, is_iheart)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(show_id, platform, chart_type, snapshot_date)
        DO UPDATE SET rank = excluded.rank, is_iheart = excluded.is_iheart
        """,
        (show_id, platform, chart_type, rank, snapshot_date, int(is_iheart)),
    )


def record_video_status(conn, show_id: str, checked_date: str,
                         has_video: bool, video_url: str | None):
    """Record whether a show has a full-length video accompaniment as of a given check date."""
    conn.execute(
        """
        INSERT INTO video_status (show_id, checked_date, has_video, video_url)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(show_id, checked_date)
        DO UPDATE SET has_video = excluded.has_video, video_url = excluded.video_url
        """,
        (show_id, checked_date, int(has_video), video_url),
    )
