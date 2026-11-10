---
name: tactical-highlight-analysis
description: >-
  Use this skill when designing, tuning, or generating Football Manager (FM) style 2D tactical match
  replay coordinates, configuring off-ball player movements, tuning realistic playback speeds,
  evaluating half-space (5-zone) spatial penetrations, and formatting highlight timeline chapters.
---

# FM 2D Tactical Replay & Highlight Analysis Skill

This skill defines the technical specifications, physics rules, and analytical criteria for the project's Football Manager-style 2D tactical match replay engine (`tactics_engine.py` & `rea/fm_2d_grid_match.html`).

## 1. Core FM Match Engine Principles

### A. Dribbling & Ball Trajectory
- **No Teleportation**: Ball-carrier dribbling must use continuous interpolation (linear or Catmull-Rom/Bézier curve) across grid ticks.
- **Ball-to-Foot Proximity**: During a dribble carry, the ball coordinates must closely track the carrier's forward vector ($r \le 1.2\text{m}$) before a pass or shot release.

### B. Off-Ball Movement (Non-Involved Players)
- **Active Spatial Cohesion**: Players not directly touching the ball **must NOT freeze or stand motionless**.
- **Attacking Teammates**:
  - Make decoy runs (diverting center-backs).
  - Wing-backs make overlapping/underlapping runs in wide channels.
  - Midfielders offer passing triangles and support angles.
- **Defending Team**:
  - Backline moves in unison (stepping up for offside trap or dropping off to protect box depth).
  - Maintain compact vertical and horizontal spacing ($25\text{m} \sim 35\text{m}$ block depth).

### C. Realistic Playback Pacing & Duration
- **Playback Speed**: Base speed tuned to **$0.85\times \sim 1.0\times$** (avoid high-speed pinball / bullet motion; allow tactical analysts to observe space infiltration, body shape, and passing angles).
- **Highlight Duration**: Each highlight chapter must span **$15 \sim 25$ seconds** (complete sequence: build-up/possession recovery $\rightarrow$ line-breaking progression $\rightarrow$ key pass/assist $\rightarrow$ final strike/save).

---

## 2. Half-Space (5-Zone) Grid Standards
The football pitch is divided into 5 vertical tactical corridors:
- **Zone 1**: Left Flank ($0 \le y < 14\text{m}$)
- **Zone 2**: **Left Half-Space** ($14\text{m} \le y < 31\text{m}$) - Key playmaker penetration corridor.
- **Zone 3**: Central Corridor ($31\text{m} \le y < 51\text{m}$) - High box congestion zone.
- **Zone 4**: **Right Half-Space** ($51\text{m} \le y < 68\text{m}$) - Key playmaker penetration corridor.
- **Zone 5**: Right Flank ($68\text{m} \le y \le 82\text{m}$)

> [!IMPORTANT]
> **UI Default State**: The Half-Space (5-Zone) overlay checkbox **must be UNCHECKED by default**, allowing users to toggle it on when performing deep positional play audits.

---

## 3. Timeline Chapter Bookmarking Format
Each tactical highlight must be bookmarked with the following structure:
- **Timestamp**: `[MM:SS]` (e.g. `32:15`, `64:40`, `81:20`)
- **Event Icon**:
  - `⚽` : Decisive Goal / High-xG Strike
  - `🎯` : Key Pass / Killer Through-Ball / High-xA Chance Creation
  - `🛡️` : Counter-Press Turnover / Box Block / Interception & Forward Transition
- **Player Tag**: Target analyzed player name (e.g. `[Erling Haaland]`, `[Son Heung-min]`, `[Kim Min-jae]`)
- **Tactical Narrative**: Specific action with spatial metric (e.g. `시그니처 박스 타점 결정적 득점 (xG 0.38)`)
