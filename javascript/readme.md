# JavaScript 모듈 디렉터리 가이드 (`javascript/`)

## 1. 디렉터리 개요
`javascript/` 디렉터리는 **AgencyOS Pro** 클라이언트 사이드의 전역 상태 관리, 단일 페이지 라우팅, 선수·감독 스카우팅 및 피어 비교, 2D 전술 하이라이트 매치 렌더링, AI 협상 스파링, 그리고 재무 PSR/FFP 계산 로직을 분할 관리하는 자바스크립트 모듈 모음입니다.

---

## 2. 포함된 파일 목록 및 상세 설명

### ⚡ `app.js` (애플리케이션 라이프사이클 & 라우터)
- **역할**: 전역 애플리케이션 상태(`AppState`), 해시 라우팅 함수(`showPage`), 커스텀 토스트 알림 엔진(`showToast`), 실시간 이적/부상 티커 연동을 제어합니다.
- **주요 함수**:
  - `showPage(pageId)`: URL 해시(`#scouting`, `#clients`, `#strategy`, `#tactics`, `#documents`, `#finance`, `#regulations`)와 페이지 DOM ID 간의 별칭(alias) 매핑 및 뷰 전환 처리.
  - `showToast(msg, type)`: 에이전시 업무 완료/경고/오류 알림 팝업 렌더링.

### 🔍 `scouting.js` (스카우팅 & DataMB 피어 매트릭스 엔진)
- **역할**: 유럽 5대 리그 선수 및 감독 필터링, DataMB 7-Axis 레이더 차트 갱신, 이번에 새롭게 추가된 **동포지션 피어 다각 비교 스튜디오 (`#modal-peer-comparison`)**의 비동기 데이터 통신 및 4색 오버레이 레이더 렌더링을 처리합니다.
- **주요 함수**:
  - `fetchScoutingPlayers(league, search)`: 2,761명 선수 데이터베이스 검색.
  - `runDataMBPeerCompare(playerNames, category, season)`: `/api/scout/datamb-compare` 엔드포인트를 호출하여 7대 지표 실측치, 백분위, Scouting Agent AI 브리핑 수신 및 렌더링.

### 🎬 `tactics.js` (2D 전술 하이라이트 매치 리플레이 엔진)
- **역할**: Football Manager 2D 매치 엔진을 모방하여 11v11 선수 노드와 축구공의 프레임별 좌표 보간(Interpolation), 하프스페이스(5-Zone) 침투 가시화, 재생 속도(0.5x~3.0x), 챕터별 타임라인 이동을 처리합니다.

### 🤝 `negotiation.js` (협상 스파링 & 계약 체결 관리자)
- **역할**: 구단 단장(Sporting Director) AI 페르소나와의 실시간 대화형 스파링 통신, 영입 심사 Deal Memo 6각 레이더 점수 반영, 대표 파트너 전속 계약 결재 시 사내 포트폴리오 자동 이관 처리를 전담합니다.

### 💰 `finance.js` (구단 재무 PSR 및 FIFA 에이전트 수수료 계산기)
- **역할**: 프리미어리그 PSR 3개년 누적 손실 £105M 한도 초과 여부, 선수 이적료 최대 5년 균등 감가상각비, 주급 지출액, 그리고 FIFA FFAR 에이전트 수수료 상한(3%~10%) 티어별 계산을 즉시 수행합니다.
