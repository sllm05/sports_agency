---
name: football-scouting-pitch
description: >-
  Use this skill when analyzing a football player's scouting profile, generating professional
  club sporting director pitch decks, benchmarking physical/technical radar metrics (DataMB style),
  and evaluating tactical fit, transfer valuation, and wage structures.
---

# Football Scouting Pitch & Valuation Skill

This skill guides the agent in generating high-conviction, C-Level European Club Sporting Director pitch decks for elite football players.

## Standard Operating Procedure (SOP)

### 1. Player Profile & Contractual Audit
- Extract foundational data: Full Name, Age, Primary/Secondary Positions, Dominant Foot, Current Club, Contract Expiry Date, Estimated Market Value (Transfermarkt benchmark).
- Check contract remaining length:
  - If $\le 12$ months: Target for bargain/cut-price transfer or pre-contract agreement (Bosman ruling).
  - If $18 \sim 24$ months: Prime renewal leverage window or strategic exit transfer.
  - If $\ge 36$ months: High buyout premium required.

### 2. DataMB 8-Axis Radar Benchmark
Benchmark the target player against top-tier league percentiles (0-100 score):
1. **Progressive Carries / 90**: Ability to break defensive lines with ball progression.
2. **Key Passes / 90**: Shot-creating actions and through-ball volume.
3. **Aerial Duels Win %**: Aerial dominance and set-piece utility.
4. **Defensive Duels Win %**: 1v1 ground duel efficiency.
5. **Box Touches / 90**: Penalty box presence and high-danger zone involvement.
6. **xG + xA Contribution / 90**: Expected goal & assist involvement independent of finishing luck.
7. **Pressing Efficiency / 90**: High turnovers forced within 40m of opposition goal.
8. **Top Sprint Speed (km/h)**: Burst acceleration and recovery pace.

### 3. Tactical Fit & System Alignment
Map player attributes to modern tactical systems:
- **Positional Play (Guardiola / Arteta)**: Half-space occupation, press resistance, pass-and-move tempo.
- **High-Intensity Gegenpress (Klopp / Rangnick)**: Rapid transition counter-pressing, second-ball recovery.
- **Relational Build-up (De Zerbi / Postecoglou)**: Baited pressing, inverted fullback decoy runs, third-man runs.

### 4. Financial & Amortization Feasibility
- Always call or reference the project MCP tool `calculate_psr_and_tax_breakdown`:
  - **Gross Transfer Fee**: Spread over contract length (max 5 years under UEFA/EPL amortization rules).
  - **Annual Amortization Cost** = $\text{Transfer Fee} / \min(\text{Contract Years}, 5)$.
  - **PSR Impact** = $\text{Annual Amortization} + \text{Annual Gross Wage}$.
  - **Net Wage Calculation**: Apply destination country income tax rate to guarantee net weekly wage promise to the player.

### 5. Pitch Deck Deliverable Generation
Follow the structured pitch deck template: [Pitch Deck Template](./resources/pitch_deck_template.md).
Output must include:
- Executive Summary & Transfer Rationale
- DataMB 8-Axis Metric Table
- Tactical Role & Heatmap Analysis
- Financial Breakdown (Fee, Amortization, PSR Impact, Net Weekly Wage)
- Exit Strategy & Re-sale Residual Value
