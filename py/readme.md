# Python 백엔드 서비스 디렉터리 가이드 (`py/`)

## 1. 디렉터리 개요
`py/` 디렉터리는 **AgencyOS Pro** 플랫폼의 백엔드 코어 서비스, 비동기 웹 API, SQLite 기반 로컬 벡터 데이터베이스, 실시간 축구 데이터 동기화 파이프라인, 그리고 2D 매치 리플레이 전술 좌표 시뮬레이터를 통합 관리하는 파이썬 모듈 모음입니다.

---

## 2. 포함된 파일 목록 및 상세 설명

### 🚀 `run_server.py` (FastAPI 프로덕션 서버 실행기)
- **역할**: Uvicorn ASGI 서버를 기동하여 `http://0.0.0.0:8000`에서 백엔드 API와 프론트엔드 정적 웹앱을 구동합니다.
- **실행 명령**: `python py/run_server.py` 또는 `uv run python run_server.py`

### 🌐 `api_service.py` (FastAPI 코어 REST 엔드포인트 서비스)
- **역할**: 플랫폼의 모든 백엔드 비즈니스 로직을 서빙하는 중앙 API 허브입니다.
- **주요 엔드포인트 그룹**:
  - `/api/players`: 유럽 5대 리그 2,761명 선수 조회, 검색, 백분위 산출.
  - `/api/managers`: 유럽 100명 엘리트 사령탑 조회 및 6대 역량 지표 제공.
  - `/api/scout/datamb-compare`: **DataMB 7-Axis 동포지션 피어 다각 비교 API** (지표 실측치, 백분위, Scouting Agent AI 브리핑 생성).
  - `/api/agency/clients`: 전속 고객 포트폴리오 CRUD 및 입단/방출 계약 처리.
  - `/api/negotiation/sparring`: 구단 단장 AI 페르소나와의 실시간 반대급부 스파링.
  - `/api/tactics/highlight`: 2D 전술 하이라이트 매치 리플레이 프레임 좌표 생성.
  - `/api/rag/search`: FIFA 규정집 시맨틱 벡터 RAG 지식 검색.

### ⚽ `tactics_engine.py` (2D 전술 매치 리플레이 엔진)
- **역할**: 경기장 그리드(100x68) 상에서 11v11 선수의 오프더볼 움직임과 패스/슈팅 궤적을 30FPS로 보간 시뮬레이션하고, 하프스페이스(5-Zone) 공간 침투 점수를 계산합니다.

### 🔄 `live_sync.py` (실시간 이적 시세 & 부상 뉴스 수집 파이프라인)
- **역할**: 유럽 5대 리그 주요 이적 루머, 경기/훈련 부상 결장자 리포트, 그리고 트랜스퍼마크트 실시간 시세를 백그라운드에서 크롤링/동기화합니다.

### 📚 `sqlite_vector_store.py` (FIFA 규정집 벡터 DB 엔진)
- **역할**: FIFA FFAR, RSTP, Clearing House 등 7대 핵심 규정 PDF 문서를 청킹(Chunking)하여 임베딩하고, 고속 코사인 유사도 검색을 수행하는 RAG 벡터 스토어입니다.

### 🧪 `test_rag_pipeline.py` & `poc_agency_desk.py` (파이프라인 검증 스크립트)
- **역할**: 벡터 DB 임베딩 무결성 및 CLI 기반 에이전시 업무 프로세스 단위 테스트 스크립트입니다.
