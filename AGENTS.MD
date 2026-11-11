# AgencyOS Pro - 자율 멀티 에이전트 시스템 아키텍처 및 운용 규격서 (AGENTS.MD)

---

## 1. 멀티 에이전트 시스템 개요 (System Overview)

**AgencyOS Pro**는 글로벌 프로 축구 에이전시의 복합적인 업무(선수·감독 발굴, 피어 매트릭스 비교, 구단 이적 협상, FIFA 법률 및 FA 워크퍼밋 감사, 재무 PSR 계산, 전술 하이라이트 분석, 계약 체결)를 사람의 개입 없이 전문적이고 유기적으로 수행하기 위해 구축된 **LangGraph 기반 자율 멀티 에이전트 오케스트레이션 플랫폼**입니다.

모든 에이전트는 환각(Hallucination)을 원천 차단하고 실제 유럽 프로 축구 현장에서 사용되는 정량 데이터(DataMB 실측 백분위, Opta xT, 트랜스퍼마크트 실시간 시세, SQLite Vector DB 기반 FIFA 공식 규정집 원문)만을 근거로 결정을 내립니다.

---

## 2. 7대 전문 자율 에이전트 상세 명세 (Agent Specifications)

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                      AgencyOS Pro 자율 멀티 에이전트 오케스트레이션 파이프라인                 │
├────────────────────────────────────────────────────────────────────────────────────────┤
│                                [Chief Supervisor Agent]                                │
│                     (고객 발굴 의뢰 접수 및 전 프로세스 상태 제어)                             │
│                                           │                                            │
│            ┌──────────────────────────────┼──────────────────────────────┐             │
│            ▼                              ▼                              ▼             │
│  [Scouting Analyst Agent]    [Negotiation Sparring Agent]   [Legal Compliance Agent]   │
│  - DataMB 7-Axis 레이더       - 구단 단장 페르소나 공방        - FIFA FFAR 수수료 상한     │
│  - 동포지션 4인 피어 비교       - 6각 영입 다각도 심사         - UK FA GBE 15점 자동 심사  │
│  - 전술 롤 적합도 판정         - 이적료/주급 반대급부 조율     - EPL PSR £105M 감사        │
│            │                              │                              │             │
│            └──────────────────────────────┼──────────────────────────────┘             │
│                                           ▼                                            │
│                             [Career Strategist Agent]                                  │
│                             - 에이징 커브 및 출전 시간 시뮬레이션                      │
│                                           │                                            │
│                                           ▼                                            │
│                             [Document Writer Agent]                                    │
│                             - Deal Memo & PFA 표준 계약서 발행                         │
│                                           │                                            │
│                                           ▼                                            │
│                          [Portfolio CRM & Execution Desk]                              │
│                          - 사내 전속 계약 공식 체결 및 자산 이관                       │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

### 1) 총괄 수석 에이전트 (Chief Executive Supervisor Agent)
- **파일**: [`agent/supervisor.py`](file:///c:/AI-Native-Agent/sports_agency/agent/supervisor.py) / [`src/sports_agency/agents/supervisor.py`](file:///c:/AI-Native-Agent/sports_agency/src/sports_agency/agents/supervisor.py)
- **페르소나**: 글로벌 톱티어 스포츠 에이전시의 대표 파트너(Managing Director).
- **핵심 역할**:
  - 의뢰 유입 시 적정 타깃의 포지션 카테고리(`FW`, `ST`, `CM`, `CB`, `FB`, `GK`, `MGR`) 자동 분류.
  - 스카우팅 -> 스파링 협상 -> 법률/재무 검증 -> 커리어 분석 -> 계약서 발행 각 단계별 에이전트 호출 및 데이터 파이프라인 상태 머신 전이.
  - 최종 딜 메모(Deal Memorandum) 결재 승인권 행사.

### 2) 데이터 스카우트 분석 에이전트 (DataMB Talent Scouting Analyst Agent)
- **파일**: [`agent/scouting_analyst.py`](file:///c:/AI-Native-Agent/sports_agency/agent/scouting_analyst.py)
- **페르소나**: 데이터 및 통계 기반 수석 스카우트 분석관.
- **핵심 역할**:
  - 유럽 5대 리그 2,761명 선수에 대한 DataMB 7-Axis 핵심 지표(키패스, 크로스, 볼 운반, 드리블, NPG, npxG+xA, 어시스트) 실측치 및 유럽 백분위 산출.
  - **동포지션 피어 다각 비교 판정 (DataMB Matrix)**: 타깃 선수와 동포지션 최정상급 선수 2~3인 간의 7대 지표 오버레이 레이더 및 1위 지표 왕관(`👑`) 표 비교 분석.
  - **감독 전용 지표 분석 (Manager Tactical Matrix)**: 선수의 골/어시스트 지표와 완전히 분리된 6대 사령탑 지휘 역량(승률·PPG, 전술 유연성, 공격 전술력, 수비 조직력, 유망주 육성, 경기 운영·장악력) 정량 평가.

### 3) 구단 단장 협상 스파링 에이전트 (Sporting Director Sparring Agent)
- **파일**: [`agent/negotiation_sparring.py`](file:///c:/AI-Native-Agent/sports_agency/agent/negotiation_sparring.py)
- **페르소나**: 유럽 빅클럽의 강경하고 재정 건전성을 최우선시하는 구단 단장(Sporting Director).
- **핵심 역할**:
  - 에이전트가 제시한 이적료 및 주급에 대해 이적료 삭감, 주급 인하, 성과급/보너스 옵션 위주의 반대급부(Counter-Offer) 제시.
  - 에이전트의 논리적 반박 및 데이터 근거 제시 시 양보율(Concession Rate) 계산.
  - 영입 심사 6각 매트릭스(온피치 포텐셜, 글로벌 스타성, 재무 ROI, 신체 내구성, 규제·GBE, 캠프 안정성) 점수 채점.

### 4) 법률 및 워크퍼밋 감사 에이전트 (Legal & FA GBE Compliance Auditor Agent)
- **파일**: [`agent/legal_compliance.py`](file:///c:/AI-Native-Agent/sports_agency/agent/legal_compliance.py)
- **스킬**: [`fifa-legal-compliance`](file:///c:/AI-Native-Agent/sports_agency/.agents/skills/fifa-legal-compliance/SKILL.md)
- **핵심 역할**:
  - **FIFA FFAR 규정 감사**: 연봉 구간별 에이전트 수수료 상한선(3%~10%) 실시간 자동 적용 및 이중 대리(Dual Representation) 위반 차단.
  - **Circular 1873 판례 대응**: 독일/영국 법원 판결에 따른 상한제 잠정 유예 및 로컬 규정 리스크 안내.
  - **UK FA GBE 자동 판정**: 성인 국가대표팀 A매치 출전 비율 기반 Auto-Pass(70% 이상) 또는 15점 채점 요건 자동 검증.
  - **EPL PSR 감사**: 3개년 누적 손실 £105M 한도 내 이적료 감가상각(최대 5년) 및 연간 주급 충당 가능 여부 감사.

### 5) 커리어 및 에이징 커브 전략 에이전트 (Career Path & Aging Curve Strategist Agent)
- **파일**: [`agent/career_strategist.py`](file:///c:/AI-Native-Agent/sports_agency/agent/career_strategist.py)
- **핵심 역할**:
  - 선수의 나이별 에이징 커브와 입단 희망 구단 내 기존 주전 선수의 에이징 커브 교차점 분석.
  - 1~3년차 예상 출전 시간 확보율(Playing Time Probability) 및 챔피언스리그/유로파리그 진출 확률 산출.

### 6) 공식 계약서 & 딜 메모 작성 에이전트 (Document Writer Agent)
- **파일**: [`agent/document_writer.py`](file:///c:/AI-Native-Agent/sports_agency/agent/document_writer.py)
- **핵심 역할**:
  - 사내 전속 영입 심사 결재 보고서 (Deal Memorandum) 표준 마크다운/JSON 발행.
  - 영국 프로축구선수협회(PFA) 공식 표준 선수 대리 계약서 (Standard Football Player Contract) 조항 자동 프리필 및 PDF/인쇄 출력 포맷팅.

### 7) 재계약 및 바이아웃 분석 에이전트 (Renewal & Release Clause Analyst Agent)
- **파일**: [`agent/renewal_analyst.py`](file:///c:/AI-Native-Agent/sports_agency/agent/renewal_analyst.py)
- **핵심 역할**:
  - 계약 만료 D-18개월/D-6개월 시점 감지 및 구단과의 재계약 골든타임 알림.
  - 바이아웃(Release Clause) 상향과 주급 인상률 간의 최적 트레이드오프 수치 도출.

---

## 3. LangGraph 상태 머신 워크플로우 (Workflow Architecture)

플랫폼의 전체 업무 흐름은 [`agent/agency_workflow.py`](file:///c:/AI-Native-Agent/sports_agency/agent/agency_workflow.py)에 정의된 `AgencyWorkflowState` TypedDict를 통해 상태를 공유하며 단계적으로 전이됩니다:

```python
class AgencyWorkflowState(TypedDict):
    target_name: str
    target_type: Literal["PLAYER", "MANAGER"]
    position: str
    scouting_dossier: Dict[str, Any]
    peer_matrix: Dict[str, Any]
    sparring_history: List[Dict[str, str]]
    deal_memo_scores: Dict[str, float]
    legal_compliance_audit: Dict[str, Any]
    psr_finance_status: Dict[str, Any]
    career_curve_analysis: Dict[str, Any]
    contract_document: str
    is_signed_to_agency: bool
```

---

## 4. 전문 스킬셋 (Agent Skills)

에이전트는 `.agents/skills/` 및 `agent/skills/`에 패키징된 정밀 지식 스킬을 동적으로 호출합니다:

1. **`fifa-legal-compliance`**:
   - FIFA FFAR 조항별 수수료 상한 규칙
   - UK FA GBE 15점 채점표 매뉴얼
   - 프리미어리그 PSR £105M 및 차세대 SSR(스쿼드 비용 비율 70%) 감가상각 산식
2. **`football-scouting-pitch`**:
   - DataMB 7-Axis 레이더 벤치마크 기준선
   - 구단 단장(Sporting Director) 프레젠테이션용 피치덱 마크다운 템플릿
   - CIES Football Observatory 공정 시장가치 산출 로직
3. **`tactical-highlight-analysis`**:
   - Football Manager 2D 매치 리플레이 (100x68) 그리드 좌표 보간
   - 5-Zone 하프스페이스(좌우 하프스페이스, 중앙, 좌우 윙) 공간 침투 분석
   - 4단계 챕터 타임라인 (빌드업 -> 전개 -> 킬패스 -> 슈팅/골) 분할

---

## 5. 프로젝트 5대 디렉터리 분류 체계 (Project File Organization)

사용자 요청에 따라 프로젝트의 모든 자산은 5대 표준 디렉터리로 체계적으로 분류되었으며, 각 폴더마다 상세 가이드(`readme.md`)가 완비되어 있습니다:

| 분류 디렉터리 | 포함 자산 및 역할 | 상세 문서 |
| :--- | :--- | :--- |
| **`html/`** | 메인 웹 애플리케이션(`index.html`), 개발 진행 상황 보고서(`DEVELOPMENT_PROGRESS.html`), 마스터 플랜 문서(`SPORTS_AGENCY_V3_MASTER_PLAN.html`) | [`html/readme.md`](file:///c:/AI-Native-Agent/sports_agency/html/readme.md) |
| **`css/`** | 글로벌 다크 테마(`main.css`), DataMB 레이더 차트 스타일(`radar_charts.css`), 2D 경기장 피치 스타일(`tactics_pitch.css`), 인쇄/PDF 전용 미디어쿼리(`print.css`) | [`css/readme.md`](file:///c:/AI-Native-Agent/sports_agency/css/readme.md) |
| **`javascript/`** | 애플리케이션 라이프사이클(`app.js`), 스카우팅 & 피어 매트릭스(`scouting.js`), 2D 전술 리플레이(`tactics.js`), 협상 스파링(`negotiation.js`), 재무 PSR 계산기(`finance.js`) | [`javascript/readme.md`](file:///c:/AI-Native-Agent/sports_agency/javascript/readme.md) |
| **`py/`** | 프로덕션 서버 실행기(`run_server.py`), 코어 REST API(`api_service.py`), 2D 전술 시뮬레이터(`tactics_engine.py`), 실시간 동기화 파이프라인(`live_sync.py`), 벡터 DB(`sqlite_vector_store.py`) | [`py/readme.md`](file:///c:/AI-Native-Agent/sports_agency/py/readme.md) |
| **`agent/`** | 7대 전문 자율 에이전트 소스코드, LangGraph 워크플로우 상태 머신(`agency_workflow.py`), 그리고 3대 에이전트 스킬셋(`skills/`) | [`agent/readme.md`](file:///c:/AI-Native-Agent/sports_agency/agent/readme.md) |

---

## 6. 품질 검증 및 시스템 무결성 보증 (QA & Audit)

1. **포트폴리오 초기 상태 무결성**: 가상 테스트 데이터(`id >= 90000`, Test League)가 전수 영구 제거되었으며, 초기 0명 상태에서 사용자가 직접 계약을 체결하여 에이전시 자산으로 이관할 수 있습니다.
2. **감독 vs 선수 지표 완전 분리**: 사령탑 선택 시 6대 지휘 역량(승률, PPG, 전술 유연성, 공수 조직력, 유망주 육성, 경기 장악력)으로 자동 전환되며, 선수 선택 시 DataMB 7-Axis 지표로 정확히 분리되어 표시됩니다.
3. **동포지션 피어 다각 비교 스튜디오 탑재**: 선택 선수/감독 상세 카드에서 `[⚖️ 동포지션 피어 다각 비교 (DataMB Matrix)]` 버튼을 클릭하여 모달 형태로 4인 동시 오버레이 레이더와 비교표, Scouting Agent AI 브리핑을 즉시 열람할 수 있습니다.
4. **종합 감사 보고서**: 전체 개발 진행 상황 및 아키텍처 감사 내용은 [`DEVELOPMENT_PROGRESS.html`](file:///c:/AI-Native-Agent/sports_agency/DEVELOPMENT_PROGRESS.html)에서 시각 대시보드로 즉시 확인할 수 있습니다.
5. **에이전시 2대 비즈니스 트랙 및 5대 GNB 계층화**: 회사 관점에서 '기존 소속 고객 관리'와 '신규 고객 발굴' 트랙을 대시보드와 GNB에서 명확히 분리하고, 2D 전술 재현기 및 PSR 재무 계산기를 '이적·전술 협상 데스크'의 전문 하위 도구로 수납하여 기능 누락 없이 업무 동선을 획기적으로 정돈했습니다.
