"""
Database Loader from External Real Datasets (`data/seed_real_data.py`)

Loads structured JSON datasets (`data/datasets/*.json`) into `data/agency_desk.db`
without any inline hardcoded player/club tuples in Python code.
"""

import json
import sqlite3
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent
DATASETS_DIR = DATA_DIR / "datasets"
DB_PATH = DATA_DIR / "agency_desk.db"


def init_db() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS players (
            player_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            name_ko TEXT NOT NULL,
            is_agency_client INTEGER NOT NULL DEFAULT 0,
            current_club TEXT NOT NULL,
            league TEXT NOT NULL,
            position TEXT NOT NULL,
            secondary_positions TEXT,
            age INTEGER NOT NULL,
            nationality TEXT NOT NULL,
            is_eu_citizen INTEGER NOT NULL DEFAULT 0,
            contract_expires TEXT NOT NULL,
            market_value_eur INTEGER NOT NULL,
            weekly_wage_eur INTEGER NOT NULL,
            is_wage_estimated INTEGER NOT NULL DEFAULT 1,
            intl_match_pct REAL NOT NULL,
            continental_minutes_pct REAL NOT NULL,
            Domestic_minutes_pct REAL NOT NULL,
            current_league_band INTEGER NOT NULL,
            strengths_summary TEXT NOT NULL
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS player_stats (
            stat_id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id INTEGER NOT NULL,
            season TEXT NOT NULL,
            minutes_played INTEGER NOT NULL,
            appearances INTEGER NOT NULL,
            goals_per90 REAL NOT NULL,
            assists_per90 REAL NOT NULL,
            xg_per90 REAL NOT NULL,
            xa_per90 REAL NOT NULL,
            key_passes_per90 REAL NOT NULL,
            progressive_actions_per90 REAL NOT NULL,
            defensive_duels_won_pct REAL NOT NULL,
            pos_percentile INTEGER NOT NULL,
            FOREIGN KEY (player_id) REFERENCES players(player_id)
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS club_squad_needs (
            need_id INTEGER PRIMARY KEY AUTOINCREMENT,
            club_name TEXT NOT NULL,
            league TEXT NOT NULL,
            country TEXT NOT NULL,
            league_band INTEGER NOT NULL,
            position TEXT NOT NULL,
            current_starter TEXT NOT NULL,
            starter_age INTEGER NOT NULL,
            starter_contract_expires TEXT NOT NULL,
            starter_weekly_wage_eur INTEGER NOT NULL,
            max_transfer_fee_budget_eur INTEGER NOT NULL,
            max_weekly_wage_offer_eur INTEGER NOT NULL,
            wage_budget_tier TEXT NOT NULL,
            non_eu_slots_free INTEGER NOT NULL,
            tactical_style TEXT NOT NULL,
            recruitment_urgency TEXT NOT NULL,
            recruitment_note TEXT NOT NULL
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS gbe_scoring_rules (
            rule_type TEXT NOT NULL,
            band_or_min_pct REAL NOT NULL,
            points INTEGER NOT NULL,
            description TEXT NOT NULL
        )
        """
    )

    for tbl in ["players", "player_stats", "club_squad_needs", "gbe_scoring_rules"]:
        json_file = DATASETS_DIR / f"{tbl}.json"
        if not json_file.exists():
            continue
        rows = json.loads(json_file.read_text(encoding="utf-8"))
        if not rows:
            continue
        cur.execute(f"DELETE FROM {tbl}")
        cols = list(rows[0].keys())
        placeholders = ", ".join(["?"] * len(cols))
        col_names = ", ".join(cols)
        values = [tuple(r[c] for c in cols) for r in rows]
        cur.executemany(
            f"INSERT INTO {tbl} ({col_names}) VALUES ({placeholders})",
            values,
        )

    conn.commit()
    conn.close()
    print(f"[SUCCESS] Loaded external datasets from {DATASETS_DIR} into {DB_PATH}")


if __name__ == "__main__":
    init_db()
