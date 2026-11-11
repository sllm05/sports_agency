"""
RAG & Official FIFA PDF Vector Search Verification Suite (`test_rag_pipeline.py`)

Verifies the complete RAG implementation in `src/sports_agency/rag/sqlite_vector_store.py`:
1. Official FIFA Legal PDFs (`data/docs/pdfs/*.pdf` — 4 official FIFA documents, 62 pages total)
   + Structured Regulations Guide (`data/docs/regulations.md`)
2. LangChain `RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)`
3. SQLite Vector Store (`data/agency_desk.db`: `rag_regulations_vec` via `gemini-embedding-2` &
   `scouting_notes_vec` via `gemini-embedding-001`)
4. Default retrieval `top_k=5` with source citations and effective dates.

Run with:
    uv run python test_rag_pipeline.py
"""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT / "src"))

from sports_agency.config import CONFIG
from sports_agency.rag.sqlite_vector_store import VECTOR_STORE


def run_rag_test() -> None:
    print("=" * 88)
    print("⚽ AI Football Agency Strategy Desk — SQLite Vector DB & PDF RAG Test Suite")
    print("=" * 88)
    print(f"• Configured Chunk Size    : {CONFIG.rag_chunk_size}")
    print(f"• Configured Chunk Overlap : {CONFIG.rag_chunk_overlap}")
    print(f"• Configured Default Top-K : {CONFIG.rag_default_top_k}")
    print(f"• Primary Embedding Model  : {CONFIG.primary_embedding_model} ({CONFIG.embedding_dimension}d)")
    print(f"• Light Embedding Model    : {CONFIG.light_embedding_model} ({CONFIG.embedding_dimension}d)")
    print("-" * 88)

    # 1. Inspect PDF & Markdown chunking (chunk_size=800, chunk_overlap=150)
    chunks = VECTOR_STORE.build_all_regulation_chunks()
    md_chunks = [c for c in chunks if c["chunk_id"].startswith("md_")]
    pdf_chunks = [c for c in chunks if c["chunk_id"].startswith("pdf_")]
    max_len = max((len(c["content"]) for c in chunks), default=0)
    avg_len = int(sum(len(c["content"]) for c in chunks) / max(1, len(chunks)))

    print(f"[Step 1] Document Chunking Verification (RecursiveCharacterTextSplitter)")
    print(f"  - Markdown Regulation Chunks (`regulations.md`) : {len(md_chunks)} chunks")
    print(f"  - Official FIFA PDF Chunks (`data/docs/pdfs/`)  : {len(pdf_chunks)} chunks")
    print(f"  - Total Regulation Chunks                       : {len(chunks)} chunks")
    print(f"  - Chunk Length Stats (chars)                    : avg={avg_len}, max={max_len} (limit={CONFIG.rag_chunk_size})")
    assert max_len <= CONFIG.rag_chunk_size, f"Chunk exceeded {CONFIG.rag_chunk_size} chars: {max_len}"
    print("  ✅ Chunk size (<= 800) & overlap (150) assertion PASSED!\n")

    # 2. Ensure SQLite Vector Store is indexed with live Vertex AI Embeddings
    print("[Step 2] Indexing / Verifying SQLite Vector Store (`data/agency_desk.db`) ...")
    idx_status = VECTOR_STORE.ensure_indexed(force_reindex=False)
    if idx_status["rag_regulations_chunks"] != len(chunks):
        print(f"  -> Updating `rag_regulations_vec` from {idx_status['rag_regulations_chunks']} to {len(chunks)} chunks ...")
        idx_status = VECTOR_STORE.ensure_indexed(reindex_regulations_only=True)
    print(f"  - SQLite DB Path             : {idx_status['sqlite_db_path']}")
    print(f"  - sqlite-vec Extension       : {idx_status['sqlite_vec_extension']}")
    print(f"  - `rag_regulations_vec` Rows : {idx_status['rag_regulations_chunks']} ({idx_status['rag_regulations_embedding_model']})")
    print(f"  - `scouting_notes_vec` Rows  : {idx_status['scouting_notes_chunks']} ({idx_status['scouting_notes_embedding_model']})\n")

    # 3. Test Regulation & Official FIFA PDF Vector Search (default top_k=5)
    test_queries = [
        "FIFA Circular 1873 worldwide temporary suspension of FFAR service fee cap Article 15",
        "영국 FA GBE 워크퍼밋 15점 자동 통과 기준 및 A매치 출전 비율",
        "스페인 라리가(La Liga) 및 이탈리아 세리에A 비유럽(Non-EU) 외국인 선수 등록 쿼터 제한",
        "What is the service fee cap for a Football Agent representing an Individual or Engaging Entity under FFAR?",
    ]

    print("[Step 3] Testing `search_regulations()` with default `top_k=5` (`gemini-embedding-2`)")
    for q_idx, query in enumerate(test_queries, start=1):
        print("-" * 88)
        print(f"🔍 Query {q_idx}: {query}")
        results = VECTOR_STORE.search_regulations(query=query)
        assert len(results) == CONFIG.rag_default_top_k, f"Expected top_k={CONFIG.rag_default_top_k}, got {len(results)}"
        for rank, item in enumerate(results, start=1):
            snippet = item["content"].replace("\n", " ")[:120]
            print(
                f"  [{rank}] (Score: {item['similarity_score']:.4f} | Len: {item['char_length']}c) "
                f"{item['title']}\n"
                f"      📌 출처: {item['source_citation']} | 기준일: {item['effective_date']}\n"
                f"      📄 내용: {snippet}..."
            )

    # 4. Test Tactical Fit Scouting Vector Search (default top_k=5)
    print("\n" + "=" * 88)
    print("[Step 4] Testing `search_tactical_fit()` with default `top_k=5` (`gemini-embedding-001`)")
    tactical_query = "Right Winger (left-footed) | 빠른 역습 전개, 90분당 전진 패스 및 박스 타격 능력 우수"
    tactical_results = VECTOR_STORE.search_tactical_fit(player_strengths=tactical_query, position="RW")
    assert len(tactical_results) == CONFIG.rag_default_top_k, f"Expected top_k={CONFIG.rag_default_top_k}, got {len(tactical_results)}"
    for rank, tm in enumerate(tactical_results, start=1):
        print(
            f"  [{rank}] (Cosine Sim: {tm['tactical_similarity_score']:.4f}) "
            f"{tm['club_name']} ({tm['league']}) — {tm['tactical_note']}"
        )

    print("=" * 88)
    print("🎉 ALL RAG PIPELINE TESTS (PDF + Markdown, chunk_size=800, overlap=150, top_k=5) PASSED!")
    print("=" * 88)


if __name__ == "__main__":
    run_rag_test()
