# HTML 디렉터리 가이드 (`html/`)

## 1. 디렉터리 개요
`html/` 디렉터리는 **AgencyOS Pro** 플랫폼의 모든 웹 사용자 인터페이스(UI), 마스터 아키텍처 기획 문서, 그리고 개발 진행 상황 감사 대시보드 파일을 통합 관리하는 디렉터리입니다. Tailwind CSS 및 Chart.js를 기반으로 구성되어 있으며, SPA(Single Page Application) 반응형 구조를 제공합니다.

---

## 2. 포함된 파일 목록 및 상세 설명

### 📄 `index.html` (AgencyOS Pro 통합 단일 페이지 애플리케이션)
- **역할**: 플랫폼의 메인 통합 프론트엔드 인터페이스입니다.
- **주요 페이지 및 컴포넌트 구조**:
  - `page-scouting`: 유럽 5대 리그 2,761명 선수 및 100명 사령탑 스카우팅 센터, DataMB 7-Axis 레이더, **동포지션 피어 다각 비교 스튜디오 (`#modal-peer-comparison`)**, 관심 타깃 리스트(Watchlist).
  - `page-clients`: 전속 고객 관리 포트폴리오 CRM (계약 만료 추적, 주급 총계, 원클릭 구단 입단 계약 체결 및 FA 방출 관리).
  - `page-strategy`: AI 이적 협상 스파링 데스크, 구단 단장 페르소나 실시간 공방, 사내 영입 심사 Deal Memo 승인.
  - `page-tactics`: Football Manager 스타일 2D 전술 하이라이트 매치 리플레이 엔진 (5-Zone 하프스페이스 공간 침투, 0.5x~3x 배속 조절).
  - `page-documents`: PFA 표준 축구선수 계약서 프리뷰 및 원클릭 인쇄/PDF 다운로드 센터.
  - `page-finance`: 프리미어리그 PSR 3개년 £105M Waterfall 차트 및 FIFA FFAR 에이전트 수수료 상한 계산기.
  - `page-regulations`: SQLite Vector DB 기반 FIFA FFAR, RSTP, UK FA GBE 규정집 시맨틱 RAG 지식 검색.
  - `#modal-peer-comparison`: 이번에 추가된 동포지션 4인 동시 DataMB 7축 오버레이 레이더 + 매트릭스 비교표 + Scouting Agent AI 종합 브리핑 모달.
  - `#modal-briefing-center`: 5대 리그 실시간 부상자 및 이적 루머 모니터링 센터.

### 📄 `DEVELOPMENT_PROGRESS.html` (개발 진행 상황 & 시스템 종합 감사 보고서)
- **역할**: 프로젝트의 7대 핵심 모듈 완성도(98.4%), 품질 감사 결과, 멀티 에이전트 오케스트레이션 아키텍처 다이어그램, 최신 버그 픽스 내역 및 향후 로드맵을 시각화한 대시보드 문서입니다.
- **주요 섹션**:
  - v3.0 Production Release 현황 KPI (선수 2,761명, 사령탑 100명, 7대 규정집, 5-zone 리플레이).
  - 7대 핵심 모듈별 기능 범위, 구현 상태(100%), 최신 최적화 내역 테이블.
  - LangGraph 기반 자율 멀티 에이전트(Supervisor, Scouting, Sparring, Legal, Document) 협업 흐름도.
  - 5대 폴더(`html`, `css`, `javascript`, `py`, `agent`) 재분류 구조 안내.

### 📄 `SPORTS_AGENCY_V3_MASTER_PLAN.html` (v3.0 마스터 플랜 및 기술 설계서)
- **역할**: 플랫폼의 초기 요구사항 분석, 엔터프라이즈 하이브리드 아키텍처, 데이터 스키마 및 규제 준수 프레임워크를 기술한 공식 기획 문서입니다.

---

## 3. 기술 스택 및 연동 사양
- **스타일링**: Tailwind CSS CDN, Pretendard, JetBrains Mono 웹 폰트
- **시각화 라이브러리**: Chart.js 4.4.3 (Radar, Bar, Line, Scatter Charts)
- **마크다운 렌더링**: Marked.js (AI 브리핑 및 표준 계약서 실시간 파싱)
- **통신**: RESTful Fetch API (백엔드 FastAPI 서버와 실시간 비동기 연동)
