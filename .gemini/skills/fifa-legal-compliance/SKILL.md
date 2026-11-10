---
name: fifa-legal-compliance
description: >-
  Use this skill when auditing football player contracts, checking FIFA FFAR agent fee caps,
  verifying dual representation restrictions, calculating UK FA GBE work permit points,
  and validating Premier League PSR and UEFA FFP financial compliance.
---

# FIFA Legal Compliance & Financial Audit Skill

This skill enforces strict adherence to international football governing body regulations (FIFA, FA, UEFA, Premier League) developed throughout our sports agency system.

## 1. FIFA FFAR (Football Agent Regulations) Commission Caps
When reviewing representation agreements or transfer fee commissions:
- **Client Remuneration $\le \$200,000$ / year**:
  - Representing Player or Engaging (Buyer) Club: Maximum **5%** of player remuneration.
  - Representing Both Player and Engaging Club: Maximum **10%** (5% + 5%).
  - Representing Releasing (Selling) Club: Maximum **10%** of total transfer compensation.
- **Client Remuneration $> \$200,000$ / year**:
  - Representing Player or Engaging (Buyer) Club: Maximum **3%** of player remuneration.
  - Representing Both Player and Engaging Club: Maximum **6%** (3% + 3%).
  - Representing Releasing (Selling) Club: Maximum **10%** of total transfer compensation.
- **Dual Representation Prohibition**:
  - Representing Releasing Club AND Engaging Club: **STRICTLY PROHIBITED (Absolute Void)**.
  - Representing Releasing Club AND Player: **STRICTLY PROHIBITED**.
  - Permitted Dual Agency: **Player + Engaging Club ONLY**, requiring prior explicit written consent from both parties.

## 2. UK FA Governing Body Endorsement (GBE) Work Permit
For transfers to the English Premier League or EFL Championship:
- **Pass Mark Threshold**: Minimum **15 points** required for automatic GBE approval.
- **Auto-Pass Criteria**:
  - National team in FIFA Top 50 and player participated in required % of senior competitive international matches (e.g. FIFA Top 1-10 requires $\ge 30\%$, Top 11-20 requires $\ge 40\%$).
- **Points-Based Table (if auto-pass not met)**:
  - Band 1 Leagues (EPL, La Liga, Serie A, Bundesliga, Ligue 1): High domestic minutes weight.
  - Continental Competitions: UEFA Champions League / Copa Libertadores group stage minutes.
  - Domestic League Table Finish: Title or European qualification position.
- **ESC (Elite Significant Contribution) Exception**:
  - EPL clubs allowed up to 4 ESC slots for high-potential international talents who score below 15 points.

## 3. Premier League PSR & UEFA FFP Financial Compliance
- **Amortization Cap**: Transfer fee must be amortized straight-line over a maximum of **5 years**, regardless of contract length (e.g. an 8-year contract must amortize over 5 years).
- **PSR Calculation**:
  $$\text{Annual PSR Cost} = \left(\frac{\text{Gross Transfer Fee}}{\min(\text{Contract Years}, 5)}\right) + \text{Annual Gross Salary}$$
- **3-Year Rolling PSR Loss Limit**: £105M for Premier League clubs with secure owner funding (reduced by £22M per year spent in the Championship).

## 4. Net vs Gross Wage and Taxation Table
Always apply destination jurisdiction tax deductions when structuring player wage demands:
| Country | Standard Top Marginal Income Tax Rate | Social Security & Surcharges | Special Exemption / Notes |
| :--- | :---: | :---: | :--- |
| **UK (EPL)** | 45% (above £125,140) | +2% National Insurance | Standard PAYE; image rights capped at 20% |
| **Spain (La Liga)** | 47% | ~2% Social Security | Beckham Law (24% flat up to €600k) if qualified |
| **Germany (Bundesliga)** | 45% | +5.5% Solidarity Surcharge | Kirchensteuer (Church tax 8-9% if applicable) |
| **Italy (Serie A)** | 43% | Regional IRPEF ~2-3% | Decreto Crescita repealed for new signings |
| **France (Ligue 1)** | 45% | CSG/CRDS social levies ~9.7% | Inpatriate tax regime (up to 50% exemption for 8 yrs) |
| **Saudi Arabia (SPL)** | **0%** | 0% | Completely tax-free net salary structure |
