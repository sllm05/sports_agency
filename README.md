# ⚽ AI Football Agency Strategy Desk (Hybrid v2.0)

유럽 축구 선수의 **타 구단 이적 역제의(Track A)** 및 **현 소속팀 재계약 연봉 벤치마킹(Track B)** 실무를 자동화하는 멀티 에이전트 웹 서비스입니다.

---

## 🛠️ 핵심 기술 스택 및 모델 이원화 구조

1. **GCP Vertex AI (ADC 인증 방식)**
   - **고성능 주력 LLM (`gemini-3.8-flash`)**:
     - `Node 2`: Hermes 다단계 MCP 도구 연쇄 호출 및 정량·전술 밸류에이션 분석
     - `Node 4`: 선수 에이전트 AI ↔ 구단 디렉터 AI 모의 협상(Sparring Loop)
     - `Node 5`: 투트랙 실무 문서(`Deal Prep Sheet` & `Club Pitch Deck`) 작성
   - **경량 고속 LLM (`gemini-3.5-flash`)**:
     - `Node 1`: Supervisor 요청 분석 및 Track A / Track B 조건부 라우팅
     - `Node 3`: 규정 RAG 검색 청크 요약 및 법률 가이드 생성
     - 실시간 구단 부상/이적설 검색(**Vertex AI Google Search Grounding**) 요약
2. **SQLite 통합 Vector DB (`data/agency_desk.db`)**
   - **`rag_regulations_vec` 테이블 (`gemini-embedding-2`)**: 영국 FA GBE 워크퍼밋 점수표, 유럽 5대 리그 Non-EU 쿼터, FIFA FFAR 제15조 및 Circular 1873 유예 공문, EPL PSR 감가상각 규정 임베딩
   - **`scouting_notes_vec` 테이블 (`gemini-embedding-001` / `text-embedding-004`)**: 선수별 전술 강점 및 구단 감독 전술 요구사항 유사도 매칭 임베딩
3. **LangGraph (`StateGraph` + `SqliteSaver` + `Human-in-the-Loop`)**
   - 1라운드 협상 직후 `interrupt_before=["sparring_round_2"]`를 통해 체크포인트(`data/agency_checkpoints.db`)에 상태를 저장하고, 웹 대시보드에서 사람 에이전트의 **원클릭 전략 선택(3종)**을 받아 2라운드 타결 및 최종 문서를 생성합니다.
4. **FastAPI + 모던 원클릭 대시보드 UI**
   - 선수 로스터 카드 선택, Chart.js 5축 스탯 레이더 차트, 실시간 모의 협상 채팅 중계, 원클릭 개입 버튼, 마크다운/PDF 인쇄 뷰어를 단일 서버로 제공합니다.

---

## 🚀 실행 방법

### 1. GCP ADC 인증 설정 (최초 1회)
```powershell
gcloud auth application-default login
gcloud config set project 본인_GCP_프로젝트_ID
gcloud auth application-default set-quota-project 본인_GCP_프로젝트_ID
```
*(웹 대시보드 상단 바에서도 `GCP Project ID`를 직접 입력하고 적용할 수 있습니다.)*

### 2. FastAPI 웹 서버 실행
```powershell
uv run python run_server.py
# 또는
uv run sports-agency
```
브라우저에서 **`http://127.0.0.1:8000`** 으로 접속하면 대시보드를 바로 사용할 수 있습니다.
