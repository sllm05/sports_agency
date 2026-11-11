# AI 에이전트 & 워크플로우 디렉터리 가이드 (`agent/`)

## 1. 디렉터리 개요
`agent/` 디렉터리는 **AgencyOS Pro**의 핵심인 **LangGraph 기반 자율 멀티 에이전트 오케스트레이션 시스템**과 7대 전문 에이전트(Supervisor, Scouting Analyst, Negotiation Sparring, Legal Compliance, Career Strategist, Document Writer, Renewal Analyst), 그리고 에이전트 전문 역량 스킬셋(`skills/`)을 통합 관리하는 디렉터리입니다.

---

## 2. 포함된 파일 목록 및 상세 설명

### 👑 `supervisor.py` (Chief Executive Agency Supervisor Agent)
- **페르소나**: 에이전시 총괄 수석 에이전트 (Chief Executive).
- **역할**: 고객 영입 의뢰 접수, 스카우팅-협상-법률-계약 각 전문 에이전트로의 업무 위임, 상태 그래프(State Graph) 제어, 최종 의사결정 판정.

### 🔍 `scouting_analyst.py` (DataMB Talent Scouting Analyst Agent)
- **페르소나**: 데이터 기반 프로 축구 수석 스카우트 분석관.
- **역할**: 
  - DataMB 7-Axis 레이더 지표(키패스, 크로스, 볼 운반, 드리블, NPG, npxG+xA, 어시스트) 실측치 및 유럽 리그 백분위 산출.
  - **동포지션 피어 다각 비교 판정**: 타깃 선수와 동일 포지션 2~3인 간의 정량적 우위 근거, 전술 롤 적합도, 출전 시간 표본 신뢰도 심층 브리핑 생성.

### 🥊 `negotiation_sparring.py` (Sporting Director Sparring Agent)
- **페르소나**: 유럽 빅클럽의 강경한 축구 단장 (Sporting Director).
- **역할**:
  - 실제 이적 시장 협상 시뮬레이션: 이적료 삭감, 주급 인하, 성과급 조항 추가 등 공격적 반대급부 제시.
  - 에이전트의 협상 논리 검증 및 6각 영입 다각도 심사 매트릭스(온피치 포텐셜, 글로벌 스타성, 재무 ROI, 신체 내구성, 규제·GBE, 캠프 안정성) 점수 산정.

### ⚖️ `legal_compliance.py` (FIFA Legal & FA GBE Compliance Auditor Agent)
- **페르소나**: 유럽 스포츠 전문 변호사 및 FIFA 공식 규제 준수 감사관.
- **역할**:
  - FIFA FFAR 에이전트 수수료 상한선 (3%~10%) 및 Circular 1873 상한 유예 법적 리스크 감사.
  - 이중 대리(Dual Representation) 위반 여부 판정.
  - 영국 FA GBE(Governing Body Endorsement) 취업 비자 워크퍼밋 15점 자동 심사.
  - 프리미어리그 PSR 3개년 £105M 및 차세대 SSR(스쿼드 비용 비율 70%) 준수 보증.

### 📈 `career_strategist.py` (Career Path & Aging Curve Strategist Agent)
- **페르소나**: 커리어 플래너 및 전술 적합도 수석 컨설턴트.
- **역할**:
  - 선수의 에이징 커브와 해당 구단 기존 주전 선수의 기량 하락 시점 교차 분석.
  - 주전 출전 시간 확보 확률(Playing Time Simulation) 및 유럽 대항전 진출 가능성 평가.

### 📝 `document_writer.py` (Deal Memo & PFA Standard Contract Writer Agent)
- **역할**:
  - 사내 전속 영입 심사 결재 보고서 (Deal Memorandum) 마크다운 및 JSON 발행.
  - 영국 PFA 공식 표준 축구선수 계약서 (Standard Football Player Contract) 자동 조항 완성.

### 🔄 `renewal_analyst.py` (Contract Renewal & Release Clause Analyst Agent)
- **역할**:
  - 계약 만료 18개월/6개월 전 재계약 협상 골든타임 감지, 바이아웃(Release Clause) 상향 조정 및 연봉 인상분 산출.

### 🌐 `agency_workflow.py` (LangGraph State Machine Multi-Agent Workflow)
- **역할**:
  - LangGraph의 `StateGraph`를 컴파일하여 `Scouting -> Sparring -> Compliance -> Career -> Document -> Portfolio`로 이어지는 무결점 상태 전환 오케스트레이션.

---

## 3. 에이전트 전문 스킬셋 (`skills/`)
| 스킬 디렉터리 | 주요 역량 및 담당 영역 |
| :--- | :--- |
| `fifa-legal-compliance` | FIFA FFAR 규정 감사, 이중대리 방지, UK FA GBE 15점 심사, EPL PSR £105M 재무 검증. |
| `football-scouting-pitch` | DataMB 레이더 벤치마크, 구단 단장 피치덱 템플릿, CIES 이적료 가치 밴드 분석. |
| `tactical-highlight-analysis` | FM 2D 그리드 좌표 보간, 하프스페이스(5-zone) 침투 추적, 챕터 타임라인 생성. |
