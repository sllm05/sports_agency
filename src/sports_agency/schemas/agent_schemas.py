"""
Sports Agency Agent Schemas and Workflow State (`src/sports_agency/schemas/agent_schemas.py`)

Defines Pydantic structured output models for Vertex AI Gemini responses,
and TypedDict graph state for the LangGraph multi-agent workflow.
"""

from __future__ import annotations

from typing import Any, TypedDict
from pydantic import BaseModel, Field


# ============================================================================
# Pydantic Structured Output Schemas (Vertex AI response_schema)
# ============================================================================

class LegalRagReviewSchema(BaseModel):
    non_eu_quota_result: str = Field(
        ...,
        description="타겟 구단 및 해당 리그의 Non-EU 외국인 선수 등록 쿼터 규정 판독 결과 (1~2문장)",
    )
    ffar_fee_guidance: str = Field(
        ...,
        description="FIFA FFAR 제15조 수수료 상한 및 Circular No. 1873 유예 공문 기반 방어 논리 (2~3문장)",
    )


class SparringRound1Schema(BaseModel):
    opening_ask_wage_eur: int = Field(
        ...,
        description="에이전트가 선수의 Opta 백분위, 잔여 계약, 비교군 주급을 근거로 1차 제시하는 주급(유로 정수)",
    )
    club_counter_wage_eur: int = Field(
        ...,
        description="구단 스포츠 디렉터가 PSR 장부 비용, 내구성/결장 리스크, 약점 백분위를 근거로 역제안하는 1차 주급(유로 정수)",
    )
    agent_r1: str = Field(
        ...,
        description="1라운드 선수 에이전트 AI의 오프닝 요구 대사 (Opta 실측 강점, UCL 경력, 비교군 주급 인용)",
    )
    director_r1: str = Field(
        ...,
        description="1라운드 상대 구단 스포츠 디렉터 AI의 반박 및 역제안 대사 (구단 PSR 감가상각 비용, 선수 보완점/가용률, FFAR 수수료 인용)",
    )


class SparringRound2Schema(BaseModel):
    agreed_base_wage_eur: int = Field(
        ...,
        description="2라운드 협상 끝에 최종 합의된 기본 주급(유로 정수)",
    )
    agreed_bonus_wage_eur: int = Field(
        ...,
        description="2라운드 협상 끝에 신설 합의된 주당 환산 성과/출전 보너스(유로 정수)",
    )
    release_clause_eur: int = Field(
        ...,
        description="최종 합의된 바이아웃(Release Clause) 금액(유로 정수)",
    )
    agreed_fee_pct: float = Field(
        ...,
        description="최종 합의된 에이전트 수수료율(%, 예: 6.0 ~ 7.5)",
    )
    agent_r2: str = Field(
        ...,
        description="2라운드 사람 수석 에이전트의 전략을 반영한 선수 에이전트 AI의 카운터 대사",
    )
    director_r2: str = Field(
        ...,
        description="2라운드 상대 구단 스포츠 디렉터 AI의 최종 합의 수용 대사",
    )


class TripleOutputDocsSchema(BaseModel):
    career_report_md: str = Field(
        ...,
        description="선수 및 가족 프레젠테이션용 커리어 성장 및 가치 평가 보고서 전체 마크다운 문서",
    )
    deal_prep_md: str = Field(
        ...,
        description="에이전트 내부 대외비용 협상 전략 치트시트 전체 마크다운 문서",
    )
    pitch_deck_md: str = Field(
        ...,
        description="구단 스포츠 디렉터 발송용 1-Page 선수 가치 제안서 전체 마크다운 문서",
    )


class DualOutputDocsSchema(BaseModel):
    deal_prep_md: str = Field(
        ...,
        description="에이전트 내부 대외비용 협상 전략 치트시트 전체 마크다운 문서",
    )
    pitch_deck_md: str = Field(
        ...,
        description="구단 스포츠 디렉터 발송용 1-Page 선수 가치 제안서 전체 마크다운 문서",
    )


# ============================================================================
# LangGraph Workflow State
# ============================================================================

class AgencyGraphState(TypedDict, total=False):
    player_name: str
    track_mode: str
    target_wage_increase_pct: int
    priority_goal: str
    preferred_league: str
    human_action_choice: str
    contract_override: dict[str, Any]

    supervisor_note: str
    model_usage_log: list[dict[str, str]]
    hermes_tool_trace: list[dict[str, Any]]

    player_profile: dict[str, Any]
    peer_wage_band: dict[str, Any]
    matched_clubs: list[dict[str, Any]]
    tactical_vector_matches: list[dict[str, Any]]
    live_club_news: dict[str, Any]
    psr_and_tax_breakdown: dict[str, Any]
    hermes_ai_summary: str

    career_strategy: dict[str, Any]

    rag_retrieved_chunks: list[dict[str, Any]]
    rag_legal_review: dict[str, Any]

    negotiation_metrics: dict[str, Any]
    sparring_transcript: list[dict[str, str]]

    career_report_md: str
    deal_prep_md: str
    pitch_deck_md: str
    saved_files: dict[str, str]
