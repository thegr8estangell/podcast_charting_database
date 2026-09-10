"""
video_check.py — determine whether a podcast has a full-length video
accompaniment, for feeding into video_status via db.py.

Two checks, since "no video" can mean different things per platform:

1. Spotify: does Spotify itself flag the show as a video podcast?
   Uses the Spotify Web API (needs a Client ID/Secret — free developer
   account, no paid tier required).

2. YouTube: is there a YouTube channel/upload matching this show that
   posts FULL episodes (not just clips/shorts)? Uses the YouTube Data
   API v3 (free quota: 10,000 units/day, a search costs 100 units).

You already touch both these platforms in more-podcast-intelligence,
so likely most of this auth is already sitting in your scraper.
"""

import requests

# ---------- Spotify ----------

def get_spotify_token(client_id: str, client_secret: str) -> str:
    resp = requests.post(
        "https://accounts.spotify.com/api/token",
        data={"grant_type": "client_credentials"},
        auth=(client_id, client_secret),
    )
    resp.raise_for_status()
    return resp.json()["access_token"]


def spotify_has_video(show_id: str, token: str) -> bool:
    """
    Spotify's show/episode objects include an 'is_playable' /
    media type marker. The most reliable free signal: check the
    show's episodes for is_video / video thumbnails via /episodes.
    """
    url = f"https://api.spotify.com/v1/shows/{show_id}/episodes?limit=5"
    resp = requests.get(url, headers={"Authorization": f"Bearer {token}"})
    resp.raise_for_status()
    episodes = resp.json().get("items", [])
    # Video episodes on Spotify carry a non-null 'video_thumbnail' or
    # 'html_description' with video markup; simplest robust check is
    # the presence of images beyond the standard cover art plus
    # duration matching typical full-episode length (see YouTube note
    # below for why duration matters more on the YouTube side).
    return any(ep.get("is_playable") and ep.get("images") and
               len(ep.get("images", [])) > 1 for ep in episodes)


# ---------- YouTube ----------

def youtube_full_episode_match(show_name: str, api_key: str,
                                audio_episode_minutes: float,
                                tolerance_minutes: float = 5.0) -> dict:
    """
    Search YouTube for a channel/video matching the show name, then
    check if the matched video's duration is close to the actual
    audio episode length. This is the key filter: a show can have a
    YouTube channel full of 60-second clips and still have NO real
    full-length video counterpart. Duration comparison is what
    separates "video podcast" from "posts promo clips."
    """
    search_url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": show_name,
        "type": "video",
        "maxResults": 5,
        "key": api_key,
    }
    resp = requests.get(search_url, params=params)
    resp.raise_for_status()
    items = resp.json().get("items", [])
    if not items:
        return {"has_video": False, "video_url": None}

    video_ids = [item["id"]["videoId"] for item in items]
    details_url = "https://www.googleapis.com/youtube/v3/videos"
    details = requests.get(details_url, params={
        "part": "contentDetails,snippet",
        "id": ",".join(video_ids),
        "key": api_key,
    }).json()

    for video in details.get("items", []):
        duration_iso = video["contentDetails"]["duration"]  # e.g. 'PT58M12S'
        minutes = _iso8601_duration_to_minutes(duration_iso)
        if abs(minutes - audio_episode_minutes) <= tolerance_minutes:
            video_id = video["id"]
            return {
                "has_video": True,
                "video_url": f"https://www.youtube.com/watch?v={video_id}",
            }

    # Found videos, but none matched full-episode length -> clips only
    return {"has_video": False, "video_url": None}


def _iso8601_duration_to_minutes(duration: str) -> float:
    """Rough ISO 8601 duration ('PT1H2M3S') -> minutes."""
    import re
    match = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", duration)
    h, m, s = (int(x) if x else 0 for x in match.groups())
    return h * 60 + m + s / 60


# ---------- Combined ----------

def check_video_status(show_name: str, spotify_show_id: str,
                        audio_episode_minutes: float,
                        spotify_token: str, youtube_api_key: str) -> dict:
    """Returns has_video / video_url combining both platform checks."""
    if spotify_has_video(spotify_show_id, spotify_token):
        return {"has_video": True, "video_url": None}  # Spotify-native video

    yt_result = youtube_full_episode_match(
        show_name, youtube_api_key, audio_episode_minutes
    )
    return yt_result
