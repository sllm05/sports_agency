"""
Legal & GBE Compliance RAG Specialist Agent (`src/sports_agency/agents/legal_compliance.py`)

Responsible for Node 3: Legal & GBE RAG Specialist.
Queries SQLite vector database for league-specific regulations (GBE, Non-EU Quotas,
FIFA FFAR fee caps, Bosman/RSTP Art. 18), computes dynamic GBE points,
and provides auditable legal provenance citations.
"""

from __future__ import annotations

from typing import Any

from mcp_server.football_mcp_server import calculate_gbe_points_from_db
from sports_agency.agents.base import BaseAgent
from sports_agency.config import ROUTER
from sports_agency.logger import log_work_event
from sports_agency.rag.sqlite_vector_store import VECTOR_STORE
from sports_agency.schemas.agent_schemas import AgencyGraphState, LegalRagReviewSchema


class LegalComplianceAgent(BaseAgent):
    """
    Legal & GBE Compliance RAG Specialist Agent (powered by gemini-3.5-flash & sqlite vector store).
    """

    def __init__(self) -> None:
        super().__init__(
            name="Legal & GBE Compliance Specialist",
            role_description="SQLite 벡터 RAG 기반 FIFA FFAR/RSTP, 리그별 Non-EU 쿼터 및 영국 GBE 워크퍼밋 법률 판독 전문가",
        )

    def run(self, state: AgencyGraphState) -> dict[str, Any]:
        logs = list(state.get("model_usage_log", []))
        p = state["player_profile"]
        clubs = state.get("matched_clubs", [])
        track_mode = state["track_mode"]

        target_club = (
            clubs[0]
            if (track_mode == "TRACK_A_TRANSFER" and clubs)
            else {
                "club_name": p["current_club"],
                "league": p["league"],
                "non_eu_slots_free": 99,
            }
        )

        target_league = target_club.get("league", p["league"])
        client_role = "감독(Head Coach)" if p.get("position") == "MGR" else f"프로축구선수({p.get('position')})"
        league_specific_law_terms = {
            "Premier League": "영국 FA GBE 워크퍼밋 15점 Auto-Pass ESC 예외슬롯 EPL PSR 5년 감가상각",
            "La Liga": "스페인 라리가 Non-EU 외국인 3명 쿼터 Royal Decree 1006/1985 의무 바이아웃 Release Clause",
            "Serie A": "이탈리아 세리에A Non-EU 시즌당 2명 신규 영입 제한 쿼터 세후 연봉 협상",
            "Bundesliga": "독일 분데스리가 Non-EU 외국인 무제한 등록 DFL 재정 건전성",
            "Ligue 1": "프랑스 리그1 Non-EU 4명 쿼터 LFP 바이아웃 금지 신사협정",
        }.get(target_league, f"{target_league} 외국인 쿼터 및 계약 규정")

        # 1. Retrieve regulation chunks dynamically from SQLite `rag_regulations_vec`
        rag_query = (
            f"{league_specific_law_terms}, {client_role} {track_mode}, "
            f"FIFA FFAR 제15조 에이전트 수수료 상한 유예 Circular No. 1873, "
            f"FIFA RSTP 제18조 3항 보스만 룰 계약만료 6개월 사전협상, UEFA FSR 구단 감가상각 5년 상한"
        )
        retrieved_chunks = VECTOR_STORE.search_regulations(query=rag_query, top_k=5)
        if retrieved_chunks:
            logs.append(
                {
                    "node": "Node 3: SQLite Regulation Vector Search",
                    "model": retrieved_chunks[0]["query_embedding_model"],
                }
            )

        # Extract provenance citations by category without duplicate fallback
        def _get_citation_by_category(cat: str, fallback_query: str) -> str:
            for ch in retrieved_chunks:
                if ch["doc_category"] == cat:
                    return f"[출처: {ch['source_citation']}, 기준일: {ch['effective_date']}]"
            cat_hits = VECTOR_STORE.search_regulations(query=fallback_query, top_k=1, category_filter=cat)
            if cat_hits:
                ch = cat_hits[0]
                if ch["chunk_id"] not in {c["chunk_id"] for c in retrieved_chunks}:
                    retrieved_chunks.append(ch)
                return f"[출처: {ch['source_citation']}, 기준일: {ch['effective_date']}]"
            top = retrieved_chunks[0]
            return f"[출처: {top['source_citation']}, 기준일: {top['effective_date']}]"

        gbe_source = _get_citation_by_category("GBE_WORK_PERMIT", "영국 FA GBE 워크퍼밋 점수 산정 Auto-Pass ESC")
        non_eu_source = _get_citation_by_category("NON_EU_QUOTA", f"{target_league} Non-EU 외국인 선수 등록 쿼터 슬롯")
        ffar_source = _get_citation_by_category("FIFA_FFAR_FEE", "FIFA FFAR Article 15 service fee cap Circular 1873 suspension")
        psr_source = _get_citation_by_category("PSR_CONTRACT_LAW", "EPL PSR UEFA FSR 이적료 감가상각 5년 RSTP Article 18")

        # 2. Calculate GBE points dynamically from SQLite `gbe_scoring_rules` table
        gbe_calc = calculate_gbe_points_from_db(
            intl_match_pct=float(p["intl_match_pct"]),
            continental_minutes_pct=float(p["continental_minutes_pct"]),
            league_band=int(p["current_league_band"]),
        )

        # 3. Synthesize Non-EU quota status & FIFA FFAR legal review via gemini-3.5-flash
        chunks_context = "\n\n".join(
            f"[{c['title']} | 출처: {c['source_citation']} | 기준일: {c['effective_date']}]\n{c['content']}"
            for c in retrieved_chunks
        )
        eu_status_label = "EU 시민권자 (Non-EU 쿼터 무관)" if p.get("is_eu_citizen") else f"Non-EU 국적 ({p.get('nationality', 'Unknown')})"
        legal_prompt = (
            f"아래 SQLite 벡터 DB에서 검색된 공식 규정 원문만을 근거로 다음 2가지 항목을 JSON 객체로 작성해줘:\n"
            f"1) 'non_eu_quota_result': 타겟 구단({target_club['club_name']}, 리그: {target_league}, 잔여 Non-EU 슬롯 코드: {target_club['non_eu_slots_free']})에 "
            f"{client_role}({p['name']}, 국적/자격: {eu_status_label}, 계약만료: {p.get('contract_expires', '')})를 등록할 때의 리그 외국인/Non-EU 쿼터 및 계약 규정 판독 결과 (1~2문장)\n"
            f"2) 'ffar_fee_guidance': 구단이 FIFA FFAR 제15조를 근거로 에이전트 수수료를 3%로 제한하려 할 때, "
            f"유예 공문(Circular No. 1873 등)과 출처/기준일을 들어 반박하는 법률 자문 요약 (2~3문장)\n\n"
            f"[검색된 규정 원문]\n{chunks_context}"
        )
        parsed_legal, model_used = ROUTER.generate_structured(
            legal_prompt,
            LegalRagReviewSchema,
            system_instruction="검색된 공식 규정 원문만을 근거로 정확한 법률 판독 결과를 작성하세요.",
            use_light_model=True,
            temperature=0.1,
        )
        logs.append({"node": "Node 3: Legal & GBE RAG Summary", "model": model_used})

        rag_legal_review = {
            "gbe_points": gbe_calc["total_points"],
            "gbe_work_permit_result": gbe_calc["status_summary"],
            "gbe_source": gbe_source,
            "non_eu_quota_result": parsed_legal.non_eu_quota_result,
            "non_eu_source": non_eu_source,
            "ffar_fee_guidance": parsed_legal.ffar_fee_guidance,
            "ffar_source": ffar_source,
            "psr_source": psr_source,
        }

        log_work_event(
            "LANGGRAPH_NODE_3",
            f"Completed SQLite Vector RAG & GBE calculation ({gbe_calc['total_points']} pts) for {p['name']}",
        )
        return {
            "rag_retrieved_chunks": retrieved_chunks,
            "rag_legal_review": rag_legal_review,
            "model_usage_log": logs,
        }
