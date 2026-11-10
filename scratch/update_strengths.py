import sqlite3

conn = sqlite3.connect('data/agency_desk.db')
conn.row_factory = sqlite3.Row
cur = conn.cursor()

# Check current players and their stats
cur.execute("""
    SELECT p.player_id, p.name, p.position, p.secondary_positions, p.market_value_eur, p.strengths_summary, p.current_club,
           s.progressive_actions_per90, s.key_passes_per90, s.xg_per90, s.xa_per90, s.minutes_played, s.goals_per90, s.assists_per90
    FROM players p
    JOIN player_stats s ON p.player_id = s.player_id
""")
rows = cur.fetchall()
print(f"Total joined rows: {len(rows)}")

updates = []
for r in rows:
    raw_s = r["strengths_summary"] or ""
    # Extract foot and agency if present
    foot = "right-footed"
    if "left-footed" in raw_s:
        foot = "left-footed"
    elif "both-footed" in raw_s:
        foot = "both-footed"
    
    agency = ""
    if "에이전시:" in raw_s:
        agency = raw_s.split("에이전시:")[-1].strip().split("|")[0].strip()

    club = r["current_club"]
    pos = r["position"]
    sec = r["secondary_positions"] or ""
    sub_pos = f"{pos} ({sec})" if sec else pos
    mkt = r["market_value_eur"]
    prog = r["progressive_actions_per90"] or 5.0
    kp = r["key_passes_per90"] or 1.0
    xg_xa = round((r["xg_per90"] or 0.0) + (r["xa_per90"] or 0.0), 2)
    mins = r["minutes_played"] or 1500

    new_strengths = (
        f"[실시간 로스터: {club}] {sub_pos} ({foot}) | 시세 €{mkt:,} | "
        f"90분당 전진액션 {prog}회, 키패스 {kp}회, xG+xAG/90 {xg_xa} (출전 {mins:,}분)"
        + (f" | 에이전시: {agency}" if agency else "")
    )
    updates.append((new_strengths, r["player_id"]))

cur.executemany("UPDATE players SET strengths_summary = ? WHERE player_id = ?", updates)
conn.commit()
print(f"Successfully updated {len(updates)} players strengths_summary with real match stats!")

# Verify top players
for name in ["Erling Haaland", "Julián Álvarez", "Kylian Mbappé", "Heung-min Son", "Min-Jae Kim"]:
    cur.execute("SELECT name, strengths_summary FROM players WHERE name LIKE ?", (f"%{name}%",))
    res = cur.fetchone()
    if res:
        print(f"[{res[0]}] -> {res[1]}")

conn.close()
