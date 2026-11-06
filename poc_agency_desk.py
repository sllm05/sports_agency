"""
CLI Runner for AI Football Agency Strategy Desk (`poc_agency_desk.py`)

Executes the live LangGraph (`StateGraph` + `SqliteSaver`) + SQLite Vector DB (`gemini-embedding-2` / `001`)
+ GCP Vertex AI (`gemini-3.8-flash` / `gemini-3.5-flash`) pipeline with zero hardcoded strings.
"""

import argparse
import sys
import uuid
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT / "src"))

from sports_agency.graph.agency_workflow import WORKFLOW_MANAGER
from sports_agency.logger import log_work_event


def main() -> None:
    parser = argparse.ArgumentParser(description="Run AI Football Agency Strategy Desk Workflow")
    parser.add_argument("--player", type=str, default="설영우", help="선수 이름 (예: 설영우, 손흥민, 이강인)")
    parser.add_argument(
        "--track",
        type=str,
        default="TRACK_A_TRANSFER",
        choices=["TRACK_A_TRANSFER", "TRACK_B_RENEWAL"],
        help="업무 트랙 선택",
    )
    parser.add_argument("--wage-increase", type=int, default=40, help="목표 주급 인상률 (%)")
    parser.add_argument(
        "--goal",
        type=str,
        default="유럽 5대 리그 즉시 주전 도약 + 적정 주급 확보",
        help="협상 최우선 가치",
    )
    parser.add_argument(
        "--strategy",
        type=str,
        default="OPTION_2_BONUS_AND_RELEASE_CLAUSE",
        choices=[
            "OPTION_1_HOLD_BASE_WAGE",
            "OPTION_2_BONUS_AND_RELEASE_CLAUSE",
            "OPTION_3_LOWER_RELEASE_FOR_CLUB_OFFER",
        ],
        help="Human-in-the-Loop 전략 선택",
    )
    args = parser.parse_args()

    thread_id = f"cli_{uuid.uuid4().hex[:8]}"
    print(f"\n🚀 [LangGraph Live Workflow Start] Thread={thread_id} | Player={args.player} | Track={args.track}")

    res = WORKFLOW_MANAGER.start_session(
        thread_id=thread_id,
        player_name=args.player,
        track_mode=args.track,
        target_wage_increase_pct=args.wage_increase,
        priority_goal=args.goal,
        auto_complete=True,
        human_action_choice=args.strategy,
    )
    st = res["state"]
    print("\n📌 [Node 1: Supervisor]")
    print(f"  {st['supervisor_note']}")

    print("\n🧠 [Node 2: Hermes Valuation & Scouting Summary]")
    print(f"  {st['hermes_ai_summary']}")

    print("\n⚖️ [Node 3: SQLite Vector RAG Legal & GBE Review]")
    print(f"  • GBE: {st['rag_legal_review']['gbe_work_permit_result']} {st['rag_legal_review']['gbe_source']}")
    print(f"  • Non-EU: {st['rag_legal_review']['non_eu_quota_result']} {st['rag_legal_review']['non_eu_source']}")
    print(f"  • FFAR: {st['rag_legal_review']['ffar_fee_guidance']}")

    print("\n🥊 [Node 4: Sparring Transcript]")
    for turn in st["sparring_transcript"]:
        print(f"  [{turn['round']}] {turn['speaker']}: {turn['message']}")

    print("\n📄 [Node 5: Saved Practical Documents]")
    print(f"  • Deal Prep Sheet: {st['saved_files']['internal_deal_prep_sheet']}")
    print(f"  • Club Pitch Deck: {st['saved_files']['external_club_pitch_deck']}")

    log_work_event("CLI_EXECUTION", f"Completed live CLI run for {args.player} ({args.track}) -> {st['saved_files']}")


if __name__ == "__main__":
    main()
