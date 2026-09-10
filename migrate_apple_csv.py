"""
migrate_apple_csv.py — one-time backfill: load existing podcast-intelligence
Apple chart CSV history into chart_history.db so you're not starting the
new database from zero.

ASSUMPTIONS TO CHECK (I don't have your actual CSV in front of me):
  - CSV has columns: show_name, chart_type, rank, date
    (chart_type values like 'top25', 'editors_pick', 'top_series')
  - date is already in or convertible to YYYY-MM-DD
  - show_id isn't in the CSV, so this generates a stable id from the
    show name (apple:<slugified-name>). If Apple show IDs (numeric,
    from the App Store) are available in your data instead, swap in
    that column — it's more reliable than name-based ids for
    cross-platform matching later.

Adjust the COLUMN MAP section below to match your real headers, then run:
    python migrate_apple_csv.py path/to/apple_chart_history.csv
"""

import csv
import re
import sys
from datetime import datetime

from db import get_conn, upsert_show, record_chart_entry

# ---- COLUMN MAP: edit these to match your actual CSV headers ----
COL_SHOW_NAME = "show_name"
COL_CHART_TYPE = "chart_type"
COL_RANK = "rank"
COL_DATE = "date"
# -------------------------------------------------------------


def slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def normalize_date(raw: str) -> str:
    """Try a few common formats, fall back to raising so bad rows surface loudly."""
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y", "%B %d, %Y"):
        try:
            return datetime.strptime(raw.strip(), fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    raise ValueError(f"Unrecognized date format: {raw!r}")


def migrate(csv_path: str, db_path: str = "chart_history.db"):
    conn = get_conn(db_path)
    row_count = 0
    error_count = 0

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                name = row[COL_SHOW_NAME].strip()
                show_id = f"apple:{slugify(name)}"
                date = normalize_date(row[COL_DATE])
                chart_type = row[COL_CHART_TYPE].strip().lower()
                rank = int(row[COL_RANK])

                upsert_show(conn, show_id=show_id, platform="apple",
                            name=name, feed_url=None, seen_date=date)
                record_chart_entry(conn, show_id=show_id, platform="apple",
                                    chart_type=chart_type, rank=rank,
                                    snapshot_date=date)
                row_count += 1
            except Exception as e:
                error_count += 1
                print(f"Skipped row {row}: {e}")

    conn.commit()
    conn.close()
    print(f"\nDone. Migrated {row_count} rows, {error_count} skipped.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python migrate_apple_csv.py path/to/apple_chart_history.csv")
        sys.exit(1)
    migrate(sys.argv[1])
