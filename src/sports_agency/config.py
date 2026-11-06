"""
GCP Vertex AI (ADC Authentication) & Multi-Model Configuration (`src/sports_agency/config.py`)

Enforces Project Rules:
- Uses live GCP Application Default Credentials (`gcloud auth application-default login`)
- Zero hardcoding: all model names, project IDs, and parameters are loaded from environment/config,
  and all LLM/Embedding/Grounding calls execute live against Vertex AI and log to `work.log`.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

from sports_agency.logger import log_work_event

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
load_dotenv(PROJECT_ROOT / ".env")


@dataclass
class AgencyConfig:
    use_vertexai: bool = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "true").lower() == "true"
    gcp_project: str = os.getenv("GOOGLE_CLOUD_PROJECT", "")
    gcp_location: str = os.getenv("GOOGLE_CLOUD_LOCATION", "global")

    primary_llm_model: str = os.getenv("PRIMARY_LLM_MODEL", "gemini-3.8-flash")
    light_llm_model: str = os.getenv("LIGHT_LLM_MODEL", "gemini-3.5-flash")

    primary_embedding_model: str = os.getenv("PRIMARY_EMBEDDING_MODEL", "gemini-embedding-2")
    light_embedding_model: str = os.getenv("LIGHT_EMBEDDING_MODEL", "gemini-embedding-001")
    embedding_dimension: int = int(os.getenv("EMBEDDING_DIMENSION", "768"))

    use_google_search_grounding: bool = (
        os.getenv("USE_GOOGLE_SEARCH_GROUNDING", "true").lower() == "true"
    )
    db_path: Path = PROJECT_ROOT / "data" / "agency_desk.db"
    checkpoint_db_path: Path = PROJECT_ROOT / "data" / "agency_checkpoints.db"
    docs_path: Path = PROJECT_ROOT / "data" / "docs" / "regulations.md"
    output_dir: Path = PROJECT_ROOT / "outputs"


CONFIG = AgencyConfig()


class GeminiVertexRouter:
    """
    Manages live GCP Application Default Credentials (ADC) connection to Vertex AI
    and dispatches requests to `gemini-3.8-flash`, `gemini-3.5-flash`,
    `gemini-embedding-2`, and `gemini-embedding-001`.
    """

    def __init__(self, config: AgencyConfig = CONFIG) -> None:
        self.config = config
        self._client: Any = None
        self.adc_authenticated: bool = False
        self.detected_project: str = config.gcp_project
        self.auth_status_message: str = "Not initialized"
        self._init_client()

    def _init_client(self) -> None:
        try:
            import google.auth
            from google import genai

            credentials, default_project = google.auth.default(
                scopes=["https://www.googleapis.com/auth/cloud-platform"]
            )
            quota_proj = getattr(credentials, "quota_project_id", None)
            project_id = self.config.gcp_project or default_project or quota_proj or ""

            if project_id:
                self.detected_project = project_id
                self._client = genai.Client(
                    vertexai=True,
                    project=project_id,
                    location=self.config.gcp_location,
                )
                self.adc_authenticated = True
                self.auth_status_message = (
                    f"GCP ADC 인증 활성 (Project: {project_id}, Location: {self.config.gcp_location})"
                )
                log_work_event(
                    "GCP_ADC_INIT",
                    f"Connected to Vertex AI via ADC (project={project_id}, location={self.config.gcp_location})",
                )
            else:
                self.adc_authenticated = False
                self.auth_status_message = "GCP Project ID not configured in .env or gcloud"
        except Exception as exc:
            self.adc_authenticated = False
            self.auth_status_message = f"GCP ADC Error: {exc}"

    def refresh_auth(self) -> dict[str, Any]:
        load_dotenv(PROJECT_ROOT / ".env", override=True)
        self.config.gcp_project = os.getenv("GOOGLE_CLOUD_PROJECT", self.config.gcp_project)
        self.config.gcp_location = os.getenv("GOOGLE_CLOUD_LOCATION", self.config.gcp_location)
        self._init_client()
        return self.get_status()

    def get_status(self) -> dict[str, Any]:
        return {
            "adc_authenticated": self.adc_authenticated,
            "project_id": self.detected_project or None,
            "location": self.config.gcp_location,
            "status_message": self.auth_status_message,
            "models": {
                "primary_llm": self.config.primary_llm_model,
                "light_llm": self.config.light_llm_model,
                "primary_embedding": self.config.primary_embedding_model,
                "light_embedding": self.config.light_embedding_model,
                "embedding_dimension": self.config.embedding_dimension,
            },
        }

    def generate_text(
        self,
        prompt: str,
        *,
        system_instruction: str = "",
        use_light_model: bool = False,
        temperature: float = 0.3,
        response_mime_type: str | None = None,
    ) -> tuple[str, str]:
        """
        Calls live Vertex AI `gemini-3.8-flash` (or `gemini-3.5-flash` when use_light_model=True).
        """
        if not self.adc_authenticated or self._client is None:
            raise RuntimeError(f"GCP ADC is not authenticated: {self.auth_status_message}")

        from google.genai import types

        model_name = (
            self.config.light_llm_model if use_light_model else self.config.primary_llm_model
        )
        cfg = types.GenerateContentConfig(
            temperature=temperature,
            system_instruction=system_instruction if system_instruction else None,
            response_mime_type=response_mime_type,
        )
        resp = self._client.models.generate_content(
            model=model_name,
            contents=prompt,
            config=cfg,
        )
        text = (resp.text or "").strip()
        log_work_event(
            "VERTEX_LLM_CALL",
            f"Model={model_name} | Temp={temperature} | OutputChars={len(text)}",
        )
        return text, f"{model_name} (Vertex AI ADC)"

    def generate_structured(
        self,
        prompt: str,
        schema_cls: type[Any],
        *,
        system_instruction: str = "",
        use_light_model: bool = False,
        temperature: float = 0.25,
    ) -> tuple[Any, str]:
        """
        Calls live Vertex AI with `response_schema=schema_cls` (Pydantic model)
        so the output is guaranteed to conform to the exact Pydantic schema.
        """
        if not self.adc_authenticated or self._client is None:
            raise RuntimeError(f"GCP ADC is not authenticated: {self.auth_status_message}")

        from google.genai import types

        model_name = (
            self.config.light_llm_model if use_light_model else self.config.primary_llm_model
        )
        cfg = types.GenerateContentConfig(
            temperature=temperature,
            system_instruction=system_instruction if system_instruction else None,
            response_mime_type="application/json",
            response_schema=schema_cls,
        )
        resp = self._client.models.generate_content(
            model=model_name,
            contents=prompt,
            config=cfg,
        )
        if getattr(resp, "parsed", None) is not None:
            parsed_obj = resp.parsed
        else:
            parsed_obj = schema_cls.model_validate_json((resp.text or "{}").strip())

        log_work_event(
            "VERTEX_STRUCTURED_LLM_CALL",
            f"Model={model_name} | Schema={schema_cls.__name__} | Temp={temperature}",
        )
        return parsed_obj, f"{model_name} (Vertex AI ADC + Pydantic Schema)"

    def search_with_grounding(
        self,
        query: str,
        club_name: str,
        position: str,
    ) -> dict[str, Any]:
        """
        Executes live Vertex AI Google Search Grounding using `gemini-3.5-flash`.
        """
        if not self.adc_authenticated or self._client is None:
            raise RuntimeError(f"GCP ADC is not authenticated: {self.auth_status_message}")

        from google.genai import types

        model_name = self.config.light_llm_model
        prompt = (
            f"축구 구단 '{club_name}'의 '{position}' 포지션과 관련된 최근 주전 선수 계약/노쇠화/부상 상황, "
            f"감독의 전술적 요구사항 및 이적시장 영입 타겟 동향을 검색하여 "
            f"반드시 JSON 객체로만 응답해줘. 키는 'headline'(영문 1줄 헤드라인)과 "
            f"'tactical_context'(한국어 2~3문장 구체적 전술/스쿼드 배경 설명)만 포함할 것."
        )
        cfg = types.GenerateContentConfig(
            temperature=0.2,
            tools=[types.Tool(google_search=types.GoogleSearch())],
        )
        resp = self._client.models.generate_content(
            model=model_name,
            contents=prompt,
            config=cfg,
        )
        text = (resp.text or "").strip()
        headline = f"{club_name} ({position}) Live Scouting & Transfer Intelligence"
        tactical_context = text
        if "{" in text and "}" in text:
            try:
                raw_json = text[text.find("{") : text.rfind("}") + 1]
                parsed = json.loads(raw_json)
                headline = parsed.get("headline", headline)
                tactical_context = parsed.get("tactical_context", tactical_context)
            except Exception:
                pass

        log_work_event(
            "VERTEX_GROUNDING_SEARCH",
            f"Model={model_name} | Club={club_name} | Pos={position} | Headline={headline[:60]}",
        )
        return {
            "source": f"Vertex AI Google Search Grounding ({model_name})",
            "club_name": club_name,
            "position": position,
            "headline": headline,
            "tactical_context": tactical_context,
        }

    def embed_texts(
        self,
        texts: list[str],
        *,
        use_light_model: bool = False,
    ) -> tuple[list[list[float]], str]:
        """
        Executes live Vertex AI Embedding calls (`gemini-embedding-2` or `gemini-embedding-001`).
        """
        if not self.adc_authenticated or self._client is None:
            raise RuntimeError(f"GCP ADC is not authenticated: {self.auth_status_message}")

        from google.genai import types

        dim = self.config.embedding_dimension
        model_name = (
            self.config.light_embedding_model
            if use_light_model
            else self.config.primary_embedding_model
        )
        cfg = types.EmbedContentConfig(output_dimensionality=dim)

        all_vectors: list[list[float]] = []
        batch_size = 100 if use_light_model else 1
        for i in range(0, len(texts), batch_size):
            batch = texts[i : i + batch_size]
            resp = self._client.models.embed_content(
                model=model_name,
                contents=batch if len(batch) > 1 else batch[0],
                config=cfg,
            )
            if len(resp.embeddings) == len(batch):
                all_vectors.extend(list(e.values) for e in resp.embeddings)
            else:
                for single_text in batch:
                    single_resp = self._client.models.embed_content(
                        model=model_name,
                        contents=single_text,
                        config=cfg,
                    )
                    all_vectors.append(list(single_resp.embeddings[0].values))

        log_work_event(
            "VERTEX_EMBEDDING_CALL",
            f"Model={model_name} | Count={len(all_vectors)} | Dim={dim}",
        )
        return all_vectors, f"{model_name} (Vertex AI ADC, {dim}d)"


ROUTER = GeminiVertexRouter()
