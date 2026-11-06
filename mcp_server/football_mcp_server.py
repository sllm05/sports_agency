"""
Football Agency MCP Server (`mcp_server/football_mcp_server.py`)
Exposes standardized MCP tools backed 100% by `data/agency_desk.db` and live Vertex AI Grounding:
1. get_player_complete_data
2. find_matching_clubs_for_transfer (Track A)
3. get_peer_group_wage_band (Track B)
4. search_live_club_injury_and_rumors (Live Vertex AI Google Search Grounding + SQLite Squad Data)
5. export_agency_documents (Saves Dual-Track Deal Prep Sheet & Club Pitch Deck)
+ calculate_gbe_points_from_db (Dynamic SQLite GBE rule engine)
+ list_agency_players (Roster query for Web Dashboard)
"""

import json
import sqlite3
import statistics
import sys
from pathlib import Path
from typing import Any

from mcp.server.mcpserver import MCPServer

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT / "src"))

from sports_agency.logger import log_work_event

DB_PATH = PROJECT_ROOT / "data" / "agency_desk.db"
OUTPUT_DIR = PROJECT_ROOT / "outputs"

mcp = MCPServer("Football Agency Strategy Desk MCP Server")


def _get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def list_agency_players() -> list[dict[str, Any]]:
    """Queries all players and their FBref stats from `agency_desk.db`."""
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT p.*, s.season, s.minutes_played, s.appearances,
               s.goals_per90, s.assists_per90, s.xg_per90, s.xa_per90,
               s.key_passes_per90, s.progressive_actions_per90,
               s.defensive_duels_won_pct, s.pos_percentile
        FROM players p
        LEFT JOIN player_stats s ON p.player_id = s.player_id
        ORDER BY p.market_value_eur DESC
        """
    )
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows


@mcp.tool()
def get_player_complete_data(player_name: str) -> dict[str, Any]:
    """
    [MCP Tool 1] Queries player contract, market value, Capology weekly wage,
    FBref per-90 metrics, and GBE eligibility metrics from `agency_desk.db`.
    """
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT p.*, s.season, s.minutes_played, s.appearances,
               s.goals_per90, s.assists_per90, s.xg_per90, s.xa_per90,
               s.key_passes_per90, s.progressive_actions_per90,
               s.defensive_duels_won_pct, s.pos_percentile
        FROM players p
        LEFT JOIN player_stats s ON p.player_id = s.player_id
        WHERE LOWER(p.name) LIKE LOWER(?) OR p.name_ko LIKE ?
        LIMIT 1
        """,
        (f"%{player_name}%", f"%{player_name}%"),
    )
    row = cur.fetchone()
    conn.close()

    if not row:
        raise ValueError(f"Player '{player_name}' not found in agency_desk.db")

    data = dict(row)
    log_work_event(
        "MCP_TOOL_1",
        f"get_player_complete_data({player_name}) -> club={data['current_club']}, val=€{data['market_value_eur']:,}",
    )
    return data


@mcp.tool()
def find_matching_clubs_for_transfer(
    position: str,
    max_fee_eur: int,
    target_weekly_wage_eur: int,
    preferred_league: str = "ALL",
) -> list[dict[str, Any]]:
    """
    [MCP Tool 2 - Track A] Queries `club_squad_needs` in `agency_desk.db` for target clubs
    matching the player's position, transfer fee budget, weekly wage capacity, and optional preferred league.
    """
    conn = _get_conn()
    cur = conn.cursor()
    if preferred_league and preferred_league != "ALL":
        cur.execute(
            """
            SELECT *
            FROM club_squad_needs
            WHERE position = ?
              AND league = ?
              AND max_transfer_fee_budget_eur >= ?
              AND max_weekly_wage_offer_eur >= ?
            ORDER BY
              CASE recruitment_urgency WHEN 'High' THEN 1 WHEN 'Medium' THEN 2 ELSE 3 END,
              starter_age DESC
            LIMIT 5
            """,
            (position, preferred_league, int(max_fee_eur * 0.7), int(target_weekly_wage_eur * 0.85)),
        )
    else:
        cur.execute(
            """
            SELECT *
            FROM club_squad_needs
            WHERE position = ?
              AND max_transfer_fee_budget_eur >= ?
              AND max_weekly_wage_offer_eur >= ?
            ORDER BY
              CASE recruitment_urgency WHEN 'High' THEN 1 WHEN 'Medium' THEN 2 ELSE 3 END,
              starter_age DESC
            LIMIT 5
            """,
            (position, int(max_fee_eur * 0.7), int(target_weekly_wage_eur * 0.85)),
        )
    rows = [dict(r) for r in cur.fetchall()]

    # If strict budget/preferred_league filter returns fewer than 3 clubs, rank by budget proximity & urgency
    if len(rows) < 3:
        if preferred_league and preferred_league != "ALL":
            cur.execute(
                """
                SELECT *
                FROM club_squad_needs
                WHERE position = ? AND league = ?
                ORDER BY
                  CASE recruitment_urgency WHEN 'High' THEN 1 WHEN 'Medium' THEN 2 ELSE 3 END,
                  max_weekly_wage_offer_eur DESC
                LIMIT 5
                """,
                (position, preferred_league),
            )
            rows = [dict(r) for r in cur.fetchall()]
        if not rows:
            cur.execute(
                """
                SELECT *
                FROM club_squad_needs
                WHERE position = ?
                ORDER BY
                  CASE recruitment_urgency WHEN 'High' THEN 1 WHEN 'Medium' THEN 2 ELSE 3 END,
                  max_weekly_wage_offer_eur DESC
                LIMIT 5
                """,
                (position,),
            )
            rows = [dict(r) for r in cur.fetchall()]

    conn.close()
    log_work_event(
        "MCP_TOOL_2",
        f"find_matching_clubs_for_transfer(pos={position}, fee={max_fee_eur}, wage={target_weekly_wage_eur}, league={preferred_league}) -> {len(rows)} clubs matched",
    )
    return rows


@mcp.tool()
def get_peer_group_wage_band(
    position: str,
    age: int,
    market_value_eur: int,
    exclude_player_name: str = "",
) -> dict[str, Any]:
    """
    [MCP Tool 3 - Track B] Queries `players` & `player_stats` in `agency_desk.db`
    to compute the peer group quartile wage band (Min, Q25, Median, Q75, Max).
    """
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT p.name, p.name_ko, p.current_club, p.league, p.age,
               p.market_value_eur, p.weekly_wage_eur, p.is_wage_estimated,
               s.goals_per90, s.assists_per90, s.key_passes_per90,
               s.progressive_actions_per90, s.pos_percentile
        FROM players p
        JOIN player_stats s ON p.player_id = s.player_id
        WHERE p.position = ?
          AND p.name != ?
          AND p.age BETWEEN ? AND ?
        ORDER BY ABS(p.market_value_eur - ?) ASC
        LIMIT 5
        """,
        (position, exclude_player_name, age - 4, age + 4, market_value_eur),
    )
    peers = [dict(r) for r in cur.fetchall()]
    conn.close()

    if not peers:
        raise ValueError(f"No peer players found in DB for position={position}")

    wages = sorted(p["weekly_wage_eur"] for p in peers)
    median_wage = int(statistics.median(wages))
    q25_wage = wages[max(0, len(wages) // 4)]
    q75_wage = wages[min(len(wages) - 1, (len(wages) * 3) // 4)]

    log_work_event(
        "MCP_TOOL_3",
        f"get_peer_group_wage_band(pos={position}, age={age}) -> Q25=€{q25_wage:,}, Median=€{median_wage:,}, Q75=€{q75_wage:,}",
    )
    return {
        "position": position,
        "peer_count": len(peers),
        "wage_band_eur": {
            "min": wages[0],
            "q25_conservative": q25_wage,
            "median_fair": median_wage,
            "q75_ambitious": q75_wage,
            "max": wages[-1],
        },
        "peers": peers,
    }


@mcp.tool()
def search_live_club_injury_and_rumors(club_name: str, position: str) -> dict[str, Any]:
    """
    [MCP Tool 4] Performs live web search via Vertex AI Google Search Grounding (`gemini-3.5-flash`)
    combined with SQLite `club_squad_needs` data. Contains zero hardcoded dictionaries.
    """
    from sports_agency.config import ROUTER

    grounded = ROUTER.search_with_grounding(
        query=f"{club_name} {position} injury contract transfer target tactical need",
        club_name=club_name,
        position=position,
    )

    # Also attach the database squad record if present in `club_squad_needs`
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT current_starter, starter_age, starter_contract_expires, tactical_style, recruitment_note "
        "FROM club_squad_needs WHERE LOWER(club_name) LIKE LOWER(?) AND position = ? LIMIT 1",
        (f"%{club_name}%", position),
    )
    db_row = cur.fetchone()
    conn.close()

    if db_row:
        grounded["db_squad_record"] = dict(db_row)

    log_work_event(
        "MCP_TOOL_4",
        f"search_live_club_injury_and_rumors(club={club_name}, pos={position}) -> source={grounded['source']}",
    )
    return grounded


@mcp.tool()
def calculate_gbe_points_from_db(
    intl_match_pct: float,
    continental_minutes_pct: float,
    league_band: int,
) -> dict[str, Any]:
    """
    Calculates UK FA GBE Work Permit points dynamically by querying the `gbe_scoring_rules`
    table in `data/agency_desk.db` (zero hardcoded thresholds or point dictionaries).
    """
    conn = _get_conn()
    cur = conn.cursor()

    cur.execute(
        "SELECT band_or_min_pct, points, description FROM gbe_scoring_rules WHERE rule_type = 'AUTO_PASS_INTL_PCT' LIMIT 1"
    )
    auto_rule = cur.fetchone()
    pass_threshold = int(auto_rule["points"]) if auto_rule else 15

    if auto_rule and intl_match_pct >= float(auto_rule["band_or_min_pct"]):
        conn.close()
        return {
            "total_points": pass_threshold,
            "pass_threshold": pass_threshold,
            "is_auto_pass": True,
            "passed": True,
            "status_summary": (
                f"✅ 자동 통과 (Auto-Pass, {pass_threshold}점/{pass_threshold}점) — "
                f"{auto_rule['description']} (선수 A매치 출전율: {intl_match_pct}%)"
            ),
        }

    cur.execute(
        "SELECT points, description FROM gbe_scoring_rules WHERE rule_type = 'LEAGUE_BAND' AND band_or_min_pct = ? LIMIT 1",
        (float(league_band),),
    )
    band_row = cur.fetchone()
    band_pts = int(band_row["points"]) if band_row else 0

    cur.execute(
        "SELECT points, description FROM gbe_scoring_rules WHERE rule_type = 'CONTINENTAL_PCT' AND band_or_min_pct <= ? ORDER BY band_or_min_pct DESC LIMIT 1",
        (float(continental_minutes_pct),),
    )
    cont_row = cur.fetchone()
    cont_pts = int(cont_row["points"]) if cont_row else 0

    cur.execute(
        "SELECT points, description FROM gbe_scoring_rules WHERE rule_type = 'INTL_MATCH_PCT' AND band_or_min_pct <= ? ORDER BY band_or_min_pct DESC LIMIT 1",
        (float(intl_match_pct),),
    )
    intl_row = cur.fetchone()
    intl_pts = int(intl_row["points"]) if intl_row else 0
    conn.close()

    total_pts = band_pts + cont_pts + intl_pts
    passed = total_pts >= pass_threshold
    if passed:
        summary = (
            f"✅ 합산 통과 ({total_pts}점/{pass_threshold}점) — "
            f"리그 Band {league_band}({band_pts}점) + 대륙컵({cont_pts}점) + A매치({intl_pts}점)"
        )
    else:
        summary = (
            f"⚠️ 일반 점수 미달 ({total_pts}점/{pass_threshold}점: 리그 {band_pts}점 + 대륙컵 {cont_pts}점 + A매치 {intl_pts}점) "
            f"→ 구단 ESC(Elite Significant Contribution) 예외 슬롯 적용 대상"
        )

    return {
        "total_points": total_pts,
        "pass_threshold": pass_threshold,
        "is_auto_pass": False,
        "passed": passed,
        "status_summary": summary,
    }


@mcp.tool()
def export_agency_documents(
    player_name: str,
    deal_prep_md: str,
    pitch_deck_md: str,
) -> dict[str, str]:
    """
    [MCP Tool 5] Saves the generated Deal Prep Sheet & Club Pitch Deck Markdown files to `outputs/`.
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    safe_name = player_name.lower().replace(" ", "_")
    prep_path = OUTPUT_DIR / f"{safe_name}_deal_prep_sheet.md"
    pitch_path = OUTPUT_DIR / f"{safe_name}_club_pitch_deck.md"

    prep_path.write_text(deal_prep_md, encoding="utf-8")
    pitch_path.write_text(pitch_deck_md, encoding="utf-8")

    log_work_event(
        "MCP_TOOL_5",
        f"export_agency_documents({player_name}) -> saved {prep_path.name} & {pitch_path.name}",
    )
    return {
        "status": "saved",
        "internal_deal_prep_sheet": str(prep_path),
        "external_club_pitch_deck": str(pitch_path),
    }


HERMES_MCP_TOOLS = {
    "get_player_complete_data": get_player_complete_data,
    "find_matching_clubs_for_transfer": find_matching_clubs_for_transfer,
    "get_peer_group_wage_band": get_peer_group_wage_band,
    "search_live_club_injury_and_rumors": search_live_club_injury_and_rumors,
    "export_agency_documents": export_agency_documents,
}

if __name__ == "__main__":
    mcp.run()
