# CSS 스타일시트 디렉터리 가이드 (`css/`)

## 1. 디렉터리 개요
`css/` 디렉터리는 **AgencyOS Pro**의 다크 럭셔리(Dark Luxury) 스포츠 매니지먼트 디자인 시스템, DataMB 시각화 팔레트, 2D 축구 피치 렌더링 스타일, 그리고 PFA 표준 계약서 인쇄(Print/PDF) 미디어 쿼리를 전담하는 스타일시트 모듈 디렉터리입니다.

---

## 2. 포함된 파일 목록 및 상세 설명

### 🎨 `main.css` (글로벌 코어 디자인 시스템)
- **역할**: 전역 기본 테마 CSS 변수(`--bg-dark: #0b0d12`, `--card-dark: #11141a`), 폰트 정의(Pretendard & JetBrains Mono), 글래스모피즘 카드(`ui-card`), 커스텀 스크롤바(`custom-scrollbar`), 상태 뱃지 클래스를 정의합니다.
- **주요 속성**:
  - 다크 배경 및 2단계 중첩 카드 명도 제어.
  - 고대비 상태 인디케이터(에메랄드, 인디고, 앰버, 로즈).

### 📊 `radar_charts.css` (DataMB 레이더 & 매트릭스 스타일)
- **역할**: Chart.js 캔버스 레이아웃 래퍼, DataMB 정규 4색 시그니처 팔레트(Crimson Red `#ef4444`, Royal Blue `#3b82f6`, Emerald Green `#10b981`, Purple `#a855f7`) 클래스, 그리고 비교표 1위 지표 왕관(`👑`) 하이라이트 스타일을 정의합니다.

### ⚽ `tactics_pitch.css` (2D 전술 피치 및 하이라이트 매치 엔진)
- **역할**: Football Manager 스타일 2D 경기장 방사형 그라디언트 잔디, 5-Zone 하프스페이스 점선 분할, 11v11 홈/어웨이/타깃 선수 원형 노드(`player-node`), 축구공 물리 노드(`ball-node`)의 비주얼 스타일을 정의합니다.

### 🖨️ `print.css` (인쇄 및 PDF 내보내기 전용 스타일시트)
- **역할**: PFA 표준 선수 대리 계약서 및 영입 심사 Deal Memo 인쇄 시, 네비게이션과 버튼 등 불필요한 UI를 숨기고 흰색 배경의 고품질 오피셜 문서 규격(11pt 흑백, 표 보더, 페이지 브레이크)으로 전환합니다.

---

## 3. 디자인 토큰 사양
| 토큰명 | 색상 코드 | 용도 |
| :--- | :--- | :--- |
| `Dark Canvas` | `#0b0d12` | 전체 페이지 캔버스 배경 |
| `Card Base` | `#11141a` | 1차 컴포넌트 컨테이너 |
| `Card Inner` | `#0e1117` | 내부 통계 및 지표 패널 |
| `DataMB Red` | `#ef4444` | 타깃 영입 선수 강조 (Crimson Red) |
| `DataMB Blue` | `#3b82f6` | 1순위 피어 비교선수 (Royal Blue) |
| `DataMB Green` | `#10b981` | 2순위 피어 / 시스템 주조색 (Emerald Green) |
| `DataMB Purple`| `#a855f7` | 3순위 피어 / 감독 지휘역량 (Purple) |
