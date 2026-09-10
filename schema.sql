-- Podcast chart + video history database
-- One file, committed to the repo alongside the scraper code.

CREATE TABLE IF NOT EXISTS shows (
    show_id     TEXT PRIMARY KEY,   -- platform's native show/podcast id
    platform    TEXT NOT NULL,      -- 'spotify' | 'apple' | 'youtube' | 'podcast_index'
    name        TEXT NOT NULL,
    feed_url    TEXT,               -- RSS feed if known, helps cross-platform matching
    first_seen  TEXT NOT NULL       -- ISO date this show first appeared in any scrape
);

CREATE TABLE IF NOT EXISTS chart_entries (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    show_id       TEXT NOT NULL REFERENCES shows(show_id),
    platform      TEXT NOT NULL,     -- 'spotify' | 'apple'
    chart_type    TEXT NOT NULL,     -- 'top10' | 'top25' | 'top_series' | 'editors_pick' | etc
    rank          INTEGER NOT NULL,
    snapshot_date TEXT NOT NULL,     -- ISO date (YYYY-MM-DD), one row per show per chart per day
    is_iheart     INTEGER NOT NULL DEFAULT 0,  -- 1 if show matched the iHeart identifier list
    UNIQUE(show_id, platform, chart_type, snapshot_date)
);

CREATE TABLE IF NOT EXISTS video_status (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    show_id       TEXT NOT NULL REFERENCES shows(show_id),
    checked_date  TEXT NOT NULL,     -- ISO date this check ran
    has_video     INTEGER NOT NULL,  -- 0 or 1
    video_url     TEXT,              -- YouTube channel/video url if found
    UNIQUE(show_id, checked_date)
);

-- Helpful indexes for the "new to top X this year" queries
CREATE INDEX IF NOT EXISTS idx_chart_show_date ON chart_entries(show_id, snapshot_date);
CREATE INDEX IF NOT EXISTS idx_chart_type_date ON chart_entries(chart_type, snapshot_date);
CREATE INDEX IF NOT EXISTS idx_video_show_date ON video_status(show_id, checked_date);
