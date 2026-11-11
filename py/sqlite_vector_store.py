"""
SQLite Unified Vector DB (`src/sports_agency/rag/sqlite_vector_store.py`)

Stores both relational football data AND vector embeddings inside `data/agency_desk.db`:
1. `rag_regulations_vec` table:
   - Embedded with `gemini-embedding-2` (High-performance multimodal/long-context model)
   - Chunking Policy: `RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)`
   - Retrieval Default: `top_k=5`
   - Ingests BOTH:
     a) Official FIFA Legal PDF Documents in `data/docs/pdfs/*.pdf` (`FIFA_Football_Agent_Regulations_FFAR.pdf`,
        `FIFA_Circular_1873_FFAR_Suspension.pdf`, `FIFA_Enclosure_1_Explanatory_Notes_FFAR.pdf`,
        `FIFA_Enclosure_2_Application_FFAR.pdf`)
     b) Structured Korean/English Regulation Guide in `data/docs/regulations.md` (UK FA GBE points,
        5-League Non-EU quotas, FIFA FFAR Art. 15 & Circular 1873, EPL PSR & UEFA FSR amortization rules).
2. `scouting_notes_vec` table:
   - Embedded with `gemini-embedding-001` (Lightweight fast text embedding model)
   - Stores player tactical profiles and club recruitment style notes for semantic tactical fit scoring.
"""

from __future__ import annotations

import json
import re
import sqlite3
from pathlib import Path
from typing import Any

import numpy as np
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader

from sports_agency.config import CONFIG, ROUTER

# Official metadata mapping for downloaded FIFA PDFs in `data/docs/pdfs/`
PDF_METADATA_MAP: dict[str, dict[str, str]] = {
    "FIFA_Football_Agent_Regulations_FFAR.pdf": {
        "doc_category": "FIFA_FFAR_FEE",
        "title": "FIFA Football Agent Regulations (FFAR Official Full Text PDF)",
        "source_citation": "FIFA Football Agent Regulations (Official FIFA PDF, 39 Pages)",
        "effective_date": "2023년 10월 1일 발효 (Circular 1873 일부 유예 병행)",
    },
    "FIFA_Circular_1873_FFAR_Suspension.pdf": {
        "doc_category": "FIFA_FFAR_FEE",
        "title": "FIFA Circular No. 1873 — FFAR Worldwide Temporary Suspension Update",
        "source_citation": "FIFA Circular no. 1873 (Zurich, 30 December 2023 Official PDF, 3 Pages)",
        "effective_date": "2023년 12월 30일 발효 ~ 2026년 현재 유효",
    },
    "FIFA_Enclosure_1_Explanatory_Notes_FFAR.pdf": {
        "doc_category": "FIFA_FFAR_FEE",
        "title": "Explanatory Notes on the FIFA Football Agent Regulations (Enclosure 1)",
        "source_citation": "FIFA FFAR Explanatory Notes (Official PDF Enclosure 1, 10 Pages)",
        "effective_date": "2023-2026 시즌 기준",
    },
    "FIFA_Enclosure_2_Application_FFAR.pdf": {
        "doc_category": "FIFA_FFAR_FEE",
        "title": "Information Concerning the Application of the FIFA FFAR (Enclosure 2)",
        "source_citation": "FIFA FFAR Application Guidelines (Official PDF Enclosure 2, 10 Pages)",
        "effective_date": "2023-2026 시즌 기준",
    },
    "FIFA_Football_Agent_Regulations_FAQs.pdf": {
        "doc_category": "FIFA_FFAR_FEE",
        "title": "FIFA Football Agent Regulations Official FAQs (March 2023 Edition)",
        "source_citation": "FIFA Football Agent Regulations FAQs (Official FIFA PDF, 56 Pages)",
        "effective_date": "2023-2026 시즌 기준",
    },
    "FIFA_Regulations_Status_Transfer_Players_RSTP.pdf": {
        "doc_category": "PSR_CONTRACT_LAW",
        "title": "FIFA Regulations on the Status and Transfer of Players (RSTP Official Full Text)",
        "source_citation": "FIFA RSTP (Regulations on the Status and Transfer of Players Official PDF, 102 Pages)",
        "effective_date": "2024년 10월 / 2025-2026 시즌 발효판",
    },
    "FIFA_Clearing_House_Regulations.pdf": {
        "doc_category": "PSR_CONTRACT_LAW",
        "title": "FIFA Clearing House Regulations (Official Full Text PDF)",
        "source_citation": "FIFA Clearing House Regulations (Official FIFA PDF, 34 Pages)",
        "effective_date": "2026년 1월 발효판",
    },
}


class SQLiteAgencyVectorStore:
    """
    Unified SQLite Vector DB managing two distinct embedding spaces in `data/agency_desk.db`:
    - High-precision Regulation & FIFA PDF RAG (`gemini-embedding-2`, `chunk_size=800`, `chunk_overlap=150`, `top_k=5`)
    - Lightweight Tactical Scouting RAG (`gemini-embedding-001`)
    """

    def __init__(
        self,
        db_path: Path = CONFIG.db_path,
        docs_path: Path = CONFIG.docs_path,
        pdfs_dir: Path = CONFIG.pdfs_dir,
        chunk_size: int = CONFIG.rag_chunk_size,
        chunk_overlap: int = CONFIG.rag_chunk_overlap,
        default_top_k: int = CONFIG.rag_default_top_k,
    ) -> None:
        self.db_path = db_path
        self.docs_path = docs_path
        self.pdfs_dir = pdfs_dir
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.default_top_k = default_top_k
        self.sqlite_vec_loaded = False
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", ". ", " ", ""],
        )
        self._ensure_tables()

    def _get_conn(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA synchronous=NORMAL;")
        try:
            import sqlite_vec

            conn.enable_load_extension(True)
            sqlite_vec.load(conn)
            conn.enable_load_extension(False)
            self.sqlite_vec_loaded = True
        except Exception:
            pass
        return conn

    def _ensure_tables(self) -> None:
        conn = self._get_conn()
        cur = conn.cursor()
        # Table 1: Legal & Regulations Vector Store (gemini-embedding-2)
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS rag_regulations_vec (
                chunk_id TEXT PRIMARY KEY,
                doc_category TEXT NOT NULL,
                title TEXT NOT NULL,
                source_citation TEXT NOT NULL,
                effective_date TEXT NOT NULL,
                content TEXT NOT NULL,
                embedding_model TEXT NOT NULL,
                embedding_json TEXT NOT NULL
            )
            """
        )
        # Table 2: Player & Club Tactical Notes Vector Store (gemini-embedding-001)
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS scouting_notes_vec (
                note_id TEXT PRIMARY KEY,
                entity_type TEXT NOT NULL,
                entity_name TEXT NOT NULL,
                position TEXT NOT NULL,
                league TEXT NOT NULL,
                content TEXT NOT NULL,
                embedding_model TEXT NOT NULL,
                embedding_json TEXT NOT NULL
            )
            """
        )
        conn.commit()
        conn.close()

    def build_markdown_regulation_chunks(self) -> list[dict[str, str]]:
        """
        Parses `data/docs/regulations.md` and splits using LangChain
        RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150).
        """
        chunks: list[dict[str, str]] = []
        if not self.docs_path.exists():
            return chunks

        raw_text = self.docs_path.read_text(encoding="utf-8")
        sections = re.split(r"\n(?=## \[문서 )", raw_text)
        for idx, sec in enumerate(sections):
            sec = sec.strip()
            if not sec.startswith("## [문서"):
                continue
            lines = sec.splitlines()
            title = lines[0].replace("## ", "").strip()
            source = "FIFA / UEFA / FA Official Regulations"
            eff_date = "2024-2026 시즌"

            for line in lines[1:6]:
                if "**출처**:" in line:
                    source = line.split("**출처**:")[-1].strip()
                elif "**기준일**:" in line:
                    eff_date = line.split("**기준일**:")[-1].strip()

            split_texts = self.text_splitter.split_text(sec)
            for c_idx, chunk_text in enumerate(split_texts, start=1):
                chunks.append(
                    {
                        "chunk_id": f"md_doc_{idx}_chunk_{c_idx}",
                        "doc_category": self._infer_category(title),
                        "title": f"{title} (Part {c_idx})",
                        "source_citation": source,
                        "effective_date": eff_date,
                        "content": chunk_text.strip(),
                    }
                )
        return chunks

    def build_all_regulation_chunks(self) -> list[dict[str, str]]:
        """
        Loads BOTH `data/docs/regulations.md` AND all official PDF files in `data/docs/pdfs/*.pdf`
        and splits them using LangChain `RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)`.
        """
        chunks: list[dict[str, str]] = []

        # 1. Parse `data/docs/regulations.md` with chunk_size=800, chunk_overlap=150
        chunks.extend(self.build_markdown_regulation_chunks())

        # 2. Parse official FIFA PDFs in `data/docs/pdfs/*.pdf` with chunk_size=800, chunk_overlap=150
        if self.pdfs_dir.exists():
            for pdf_file in sorted(self.pdfs_dir.glob("*.pdf")):
                meta = PDF_METADATA_MAP.get(
                    pdf_file.name,
                    {
                        "doc_category": "FIFA_FFAR_FEE",
                        "title": pdf_file.stem.replace("_", " "),
                        "source_citation": f"Official PDF ({pdf_file.name})",
                        "effective_date": "2023-2026 시즌 기준",
                    },
                )
                try:
                    reader = PdfReader(str(pdf_file))
                except Exception:
                    continue

                full_pdf_pages: list[tuple[int, str]] = []
                for page_num, page in enumerate(reader.pages, start=1):
                    page_text = (page.extract_text() or "").strip()
                    if len(page_text) >= 40:
                        full_pdf_pages.append((page_num, page_text))

                # Split page text with RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
                pdf_chunk_counter = 0
                for page_num, page_text in full_pdf_pages:
                    page_chunks = self.text_splitter.split_text(page_text)
                    for pc in page_chunks:
                        pc_clean = pc.strip()
                        if len(pc_clean) < 40:
                            continue
                        pdf_chunk_counter += 1
                        chunks.append(
                            {
                                "chunk_id": f"pdf_{pdf_file.stem.lower()}_p{page_num}_c{pdf_chunk_counter}",
                                "doc_category": meta["doc_category"],
                                "title": f"{meta['title']} (p.{page_num})",
                                "source_citation": f"{meta['source_citation']}, Page {page_num}",
                                "effective_date": meta["effective_date"],
                                "content": pc_clean,
                            }
                        )

        return chunks

    @staticmethod
    def _infer_category(title: str) -> str:
        t = title.lower()
        if "gbe" in t or "워크퍼밋" in t:
            return "GBE_WORK_PERMIT"
        if "non-eu" in t or "외국인" in t or "쿼터" in t:
            return "NON_EU_QUOTA"
        if "ffar" in t or "수수료" in t or "service fee" in t or "circular" in t:
            return "FIFA_FFAR_FEE"
        return "PSR_CONTRACT_LAW"

    def ensure_indexed(
        self,
        force_reindex: bool = False,
        reindex_regulations_only: bool = False,
    ) -> dict[str, Any]:
        """
        Ensures both `rag_regulations_vec` (via `gemini-embedding-2`, chunk_size=800, chunk_overlap=150)
        and `scouting_notes_vec` (via `gemini-embedding-001`) are populated in SQLite.
        """
        conn = self._get_conn()
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) as cnt FROM rag_regulations_vec")
        reg_count = cur.fetchone()["cnt"]

        cur.execute("SELECT COUNT(*) as cnt FROM scouting_notes_vec")
        scout_count = cur.fetchone()["cnt"]

        reg_model_used = CONFIG.primary_embedding_model
        scout_model_used = CONFIG.light_embedding_model

        if force_reindex or reindex_regulations_only or reg_count == 0:
            chunks = self.build_all_regulation_chunks()
            if chunks:
                texts = [f"{c['title']}\n출처: {c['source_citation']}\n{c['content']}" for c in chunks]
                vectors, reg_model_used = ROUTER.embed_texts(texts, use_light_model=False)
                cur.execute("DELETE FROM rag_regulations_vec")
                for chunk, vec in zip(chunks, vectors):
                    cur.execute(
                        """
                        INSERT INTO rag_regulations_vec
                        (chunk_id, doc_category, title, source_citation, effective_date, content, embedding_model, embedding_json)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            chunk["chunk_id"],
                            chunk["doc_category"],
                            chunk["title"],
                            chunk["source_citation"],
                            chunk["effective_date"],
                            chunk["content"],
                            reg_model_used,
                            json.dumps(vec),
                        ),
                    )
                reg_count = len(chunks)

        if (force_reindex and not reindex_regulations_only) or scout_count == 0:
            cur.execute(
                "SELECT player_id, name, name_ko, position, league, strengths_summary "
                "FROM players WHERE is_agency_client = 1 OR market_value_eur >= 40000000"
            )
            players = [dict(r) for r in cur.fetchall()]
            cur.execute(
                "SELECT need_id, club_name, position, league, tactical_style, recruitment_note FROM club_squad_needs"
            )
            clubs = [dict(r) for r in cur.fetchall()]

            notes: list[dict[str, str]] = []
            for p in players:
                notes.append(
                    {
                        "note_id": f"player_{p['player_id']}",
                        "entity_type": "PLAYER",
                        "entity_name": f"{p['name_ko']} ({p['name']})",
                        "position": p["position"],
                        "league": p["league"],
                        "content": f"[{p['position']}] {p['name_ko']}: {p['strengths_summary']}",
                    }
                )
            for c in clubs:
                notes.append(
                    {
                        "note_id": f"club_{c['need_id']}",
                        "entity_type": "CLUB_NEED",
                        "entity_name": c["club_name"],
                        "position": c["position"],
                        "league": c["league"],
                        "content": f"[{c['club_name']} - {c['position']}] 전술 스타일: {c['tactical_style']} | 영입 니즈: {c['recruitment_note']}",
                    }
                )

            if notes:
                texts = [n["content"] for n in notes]
                vectors, scout_model_used = ROUTER.embed_texts(texts, use_light_model=True)
                cur.execute("DELETE FROM scouting_notes_vec")
                for note, vec in zip(notes, vectors):
                    cur.execute(
                        """
                        INSERT INTO scouting_notes_vec
                        (note_id, entity_type, entity_name, position, league, content, embedding_model, embedding_json)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            note["note_id"],
                            note["entity_type"],
                            note["entity_name"],
                            note["position"],
                            note["league"],
                            note["content"],
                            scout_model_used,
                            json.dumps(vec),
                        ),
                    )
                scout_count = len(notes)

        conn.commit()
        conn.close()
        return {
            "sqlite_db_path": str(self.db_path),
            "sqlite_vec_extension": self.sqlite_vec_loaded,
            "chunk_size": self.chunk_size,
            "chunk_overlap": self.chunk_overlap,
            "default_top_k": self.default_top_k,
            "rag_regulations_chunks": reg_count,
            "rag_regulations_embedding_model": reg_model_used,
            "scouting_notes_chunks": scout_count,
            "scouting_notes_embedding_model": scout_model_used,
        }

    def reindex_markdown_regulations_only(self) -> dict[str, Any]:
        """
        Re-indexes ONLY the markdown documents from `data/docs/regulations.md`
        into `rag_regulations_vec` without re-embedding the 679 FIFA PDF chunks.
        """
        md_chunks = self.build_markdown_regulation_chunks()
        if not md_chunks:
            return {"status": "no_chunks", "count": 0}

        texts = [f"{c['title']}\n출처: {c['source_citation']}\n{c['content']}" for c in md_chunks]
        vectors, reg_model_used = ROUTER.embed_texts(texts, use_light_model=False)

        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM rag_regulations_vec WHERE chunk_id LIKE 'md_doc_%'")
        for chunk, vec in zip(md_chunks, vectors):
            cur.execute(
                """
                INSERT OR REPLACE INTO rag_regulations_vec
                (chunk_id, doc_category, title, source_citation, effective_date, content, embedding_model, embedding_json)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    chunk["chunk_id"],
                    chunk["doc_category"],
                    chunk["title"],
                    chunk["source_citation"],
                    chunk["effective_date"],
                    chunk["content"],
                    reg_model_used,
                    json.dumps(vec),
                ),
            )
        conn.commit()
        cur.execute("SELECT COUNT(*) FROM rag_regulations_vec")
        total_count = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM rag_regulations_vec WHERE chunk_id LIKE 'md_doc_%'")
        md_count = cur.fetchone()[0]
        conn.close()
        return {
            "status": "success",
            "reindexed_md_chunks": md_count,
            "total_regulations_chunks": total_count,
            "model_used": reg_model_used,
        }

    def search_regulations(
        self,
        query: str,
        top_k: int = CONFIG.rag_default_top_k,
        category_filter: str | None = None,
    ) -> list[dict[str, Any]]:
        """
        Searches `rag_regulations_vec` using `gemini-embedding-2` query vector + cosine similarity.
        Default `top_k=5`.
        """
        self.ensure_indexed()
        q_vecs, model_used = ROUTER.embed_texts([query], use_light_model=False)
        q_vec = np.array(q_vecs[0], dtype=np.float32)
        q_norm = np.linalg.norm(q_vec) or 1.0

        conn = self._get_conn()
        cur = conn.cursor()
        if category_filter:
            cur.execute(
                "SELECT * FROM rag_regulations_vec WHERE doc_category = ?",
                (category_filter,),
            )
        else:
            cur.execute("SELECT * FROM rag_regulations_vec")
        rows = [dict(r) for r in cur.fetchall()]
        conn.close()

        results: list[dict[str, Any]] = []
        q_terms = [t for t in query.lower().split() if len(t) >= 2]

        for row in rows:
            doc_vec = np.array(json.loads(row["embedding_json"]), dtype=np.float32)
            doc_norm = np.linalg.norm(doc_vec) or 1.0
            cosine_sim = float(np.dot(q_vec, doc_vec) / (q_norm * doc_norm))

            text_lower = (row["title"] + " " + row["content"]).lower()
            keyword_hits = sum(1 for term in q_terms if term in text_lower)
            hybrid_score = round(cosine_sim + min(0.25, keyword_hits * 0.05), 4)

            results.append(
                {
                    "chunk_id": row["chunk_id"],
                    "doc_category": row["doc_category"],
                    "title": row["title"],
                    "source_citation": row["source_citation"],
                    "effective_date": row["effective_date"],
                    "content": row["content"],
                    "char_length": len(row["content"]),
                    "embedding_model": row["embedding_model"],
                    "query_embedding_model": model_used,
                    "similarity_score": hybrid_score,
                }
            )

        results.sort(key=lambda x: x["similarity_score"], reverse=True)
        return results[:top_k]

    def search_tactical_fit(
        self,
        player_strengths: str,
        position: str,
        top_k: int = CONFIG.rag_default_top_k,
    ) -> list[dict[str, Any]]:
        """
        Searches `scouting_notes_vec` using lightweight `gemini-embedding-001`
        to score semantic tactical similarity between a player's strengths and club recruitment notes.
        Default `top_k=5`.
        """
        self.ensure_indexed()
        q_vecs, model_used = ROUTER.embed_texts([player_strengths], use_light_model=True)
        q_vec = np.array(q_vecs[0], dtype=np.float32)
        q_norm = np.linalg.norm(q_vec) or 1.0

        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM scouting_notes_vec WHERE entity_type = 'CLUB_NEED' AND position = ?",
            (position,),
        )
        rows = [dict(r) for r in cur.fetchall()]
        conn.close()

        results: list[dict[str, Any]] = []
        for row in rows:
            doc_vec = np.array(json.loads(row["embedding_json"]), dtype=np.float32)
            doc_norm = np.linalg.norm(doc_vec) or 1.0
            cosine_sim = float(np.dot(q_vec, doc_vec) / (q_norm * doc_norm))
            results.append(
                {
                    "club_name": row["entity_name"],
                    "league": row["league"],
                    "position": row["position"],
                    "tactical_note": row["content"],
                    "embedding_model": model_used,
                    "tactical_similarity_score": round(cosine_sim, 4),
                }
            )

        results.sort(key=lambda x: x["tactical_similarity_score"], reverse=True)
        return results[:top_k]


VECTOR_STORE = SQLiteAgencyVectorStore()
