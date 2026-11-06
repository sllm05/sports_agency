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

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS managers (
            manager_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            current_club TEXT NOT NULL,
            league TEXT NOT NULL,
            country TEXT NOT NULL,
            age INTEGER NOT NULL,
            nationality TEXT NOT NULL,
            is_eu_citizen INTEGER NOT NULL DEFAULT 0,
            contract_expires TEXT NOT NULL,
            preferred_formation TEXT NOT NULL,
            secondary_formation TEXT NOT NULL,
            top_formations_summary TEXT NOT NULL,
            games_analyzed INTEGER NOT NULL,
            win_rate_pct REAL NOT NULL,
            points_per_game REAL NOT NULL,
            avg_goals_for REAL NOT NULL,
            avg_goals_against REAL NOT NULL,
            tactical_style TEXT NOT NULL,
            estimated_buyout_eur INTEGER NOT NULL,
            weekly_wage_eur INTEGER NOT NULL,
            tactical_flexibility_score INTEGER NOT NULL DEFAULT 75,
            attacking_coaching_score INTEGER NOT NULL DEFAULT 75,
            defensive_coaching_score INTEGER NOT NULL DEFAULT 75,
            youth_trust_score INTEGER NOT NULL DEFAULT 75,
            in_game_management_score INTEGER NOT NULL DEFAULT 75,
            leadership_personality TEXT NOT NULL DEFAULT '',
            preferred_player_profiles_json TEXT NOT NULL DEFAULT '{}'
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS transfer_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id INTEGER NOT NULL,
            player_name TEXT NOT NULL,
            transfer_date TEXT NOT NULL,
            transfer_season TEXT NOT NULL,
            from_club TEXT NOT NULL,
            to_club TEXT NOT NULL,
            transfer_fee_eur INTEGER NOT NULL,
            market_value_at_transfer_eur INTEGER NOT NULL
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS market_value_history (
            player_id INTEGER PRIMARY KEY,
            player_name TEXT NOT NULL,
            current_club TEXT NOT NULL,
            current_market_value_eur INTEGER NOT NULL,
            highest_market_value_eur INTEGER NOT NULL,
            peak_date TEXT NOT NULL,
            previous_market_value_eur INTEGER NOT NULL,
            valuation_change_pct REAL NOT NULL,
            height_cm INTEGER NOT NULL,
            preferred_foot TEXT NOT NULL,
            international_caps INTEGER NOT NULL,
            international_goals INTEGER NOT NULL,
            agency_name TEXT NOT NULL,
            recent_history_json TEXT NOT NULL
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS career_discipline_and_ucl (
            player_id INTEGER PRIMARY KEY,
            player_name TEXT NOT NULL,
            current_club TEXT NOT NULL,
            career_matches INTEGER NOT NULL,
            career_minutes INTEGER NOT NULL,
            career_goals INTEGER NOT NULL,
            career_assists INTEGER NOT NULL,
            career_yellow_cards INTEGER NOT NULL,
            career_red_cards INTEGER NOT NULL,
            ucl_matches INTEGER NOT NULL,
            ucl_goals INTEGER NOT NULL,
            ucl_assists INTEGER NOT NULL
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS club_standings_and_finances (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            competition_code TEXT NOT NULL,
            competition_name TEXT NOT NULL,
            club_name TEXT NOT NULL,
            rank_position INTEGER NOT NULL,
            played_games INTEGER NOT NULL,
            won INTEGER NOT NULL,
            draw INTEGER NOT NULL,
            lost INTEGER NOT NULL,
            points INTEGER NOT NULL,
            goals_for INTEGER NOT NULL,
            goals_against INTEGER NOT NULL,
            goal_difference INTEGER NOT NULL,
            form TEXT NOT NULL,
            stadium_name TEXT NOT NULL,
            stadium_seats INTEGER NOT NULL,
            net_transfer_record TEXT NOT NULL,
            foreigners_pct REAL NOT NULL,
            national_team_players INTEGER NOT NULL
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS competition_top_scorers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            competition_code TEXT NOT NULL,
            competition_name TEXT NOT NULL,
            rank INTEGER NOT NULL,
            player_name TEXT NOT NULL,
            nationality TEXT NOT NULL,
            club_name TEXT NOT NULL,
            played_matches INTEGER NOT NULL,
            goals INTEGER NOT NULL,
            assists INTEGER NOT NULL,
            penalties INTEGER NOT NULL
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS agency_market_share (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agency_name TEXT NOT NULL,
            big5_client_count INTEGER NOT NULL,
            total_portfolio_value_eur INTEGER NOT NULL,
            avg_client_value_eur INTEGER NOT NULL,
            top_clients_summary TEXT NOT NULL
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS player_playstyle_and_tendencies (
            player_id INTEGER PRIMARY KEY,
            player_name TEXT NOT NULL,
            current_club TEXT NOT NULL,
            position TEXT NOT NULL,
            tactical_archetype TEXT NOT NULL,
            strengths_tags TEXT NOT NULL DEFAULT '',
            weaknesses_tags TEXT NOT NULL DEFAULT '',
            progression_tendency TEXT NOT NULL,
            finishing_clinicality TEXT NOT NULL,
            temperament_and_discipline TEXT NOT NULL,
            loyalty_and_mobility TEXT NOT NULL,
            big_game_and_leadership TEXT NOT NULL,
            starter_ratio_pct REAL NOT NULL
        )
        """
    )

    for tbl in [
        "players",
        "player_stats",
        "club_squad_needs",
        "gbe_scoring_rules",
        "managers",
        "transfer_history",
        "market_value_history",
        "career_discipline_and_ucl",
        "club_standings_and_finances",
        "competition_top_scorers",
        "agency_market_share",
        "player_playstyle_and_tendencies",
    ]:
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
