import re

path = 'src/sports_agency/api/main.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update ClientRenewalPipelineRequest and ClientTransferPipelineRequest
old_models = """class ClientRenewalPipelineRequest(BaseModel):
    client_id: int = Field(..., description="재계약 대상 고객 ID")
    client_type: str = Field("PLAYER", description="PLAYER 또는 MANAGER")
    requested_weekly_wage_eur: int = Field(120000, description="요청 주급 (EUR)")
    contract_years: int = Field(3, ge=1, le=6, description="계약 연장 기간 (년)")
    requested_buyout_eur: int | None = Field(None, description="요청 바이아웃 금액 (EUR)")
    signing_bonus_eur: int = Field(0, description="계약금/서명 보너스 (EUR)")
    action: str = Field("EVALUATE", description="EVALUATE | CONFIRM_DIRECT | ACCEPT_COUNTER")


class ClientTransferPipelineRequest(BaseModel):
    client_id: int = Field(..., description="이적 대상 고객 ID")
    client_type: str = Field("PLAYER", description="PLAYER 또는 MANAGER")
    destination_club: str = Field("Tottenham Hotspur FC", description="이적 대상 구단명")
    destination_league: str = Field("Premier League", description="이적 대상 리그명")
    offered_transfer_fee_eur: int = Field(40000000, description="제안 이적료 (EUR)")
    offered_weekly_wage_eur: int = Field(140000, description="제안 주급 (EUR)")
    contract_years: int = Field(4, ge=1, le=6, description="계약 기간 (년)")
    action: str = Field("SIMULATE", description="SIMULATE | EXECUTE_TRANSFER")"""

new_models = """class ClientRenewalPipelineRequest(BaseModel):
    client_id: int = Field(..., description="재계약 대상 고객 ID")
    client_type: str = Field("PLAYER", description="PLAYER 또는 MANAGER")
    requested_weekly_wage_eur: int = Field(120000, description="요청 주급 (EUR)")
    contract_years: int = Field(3, ge=1, le=6, description="계약 연장 기간 (년)")
    requested_buyout_eur: int | None = Field(None, description="요청 바이아웃 금액 (EUR)")
    signing_bonus_eur: int | None = Field(0, description="계약금/서명 보너스 (EUR)")
    action: str = Field("EVALUATE", description="EVALUATE | CONFIRM_DIRECT | ACCEPT_COUNTER")


class ClientTransferPipelineRequest(BaseModel):
    client_id: int = Field(..., description="이적 대상 고객 ID")
    client_type: str = Field("PLAYER", description="PLAYER 또는 MANAGER")
    destination_club: str = Field("Tottenham Hotspur FC", description="이적 대상 구단명")
    destination_league: str = Field("Premier League", description="이적 대상 리그명")
    offered_transfer_fee_eur: int = Field(40000000, description="제안 이적료 (EUR)")
    offered_weekly_wage_eur: int = Field(140000, description="제안 주급 (EUR)")
    contract_years: int = Field(4, ge=1, le=6, description="계약 기간 (년)")
    action: str = Field("SIMULATE", description="SIMULATE | EVALUATE | EXECUTE_TRANSFER | FORCE_EXECUTE")"""

if old_models in content:
    content = content.replace(old_models, new_models)
    print("Updated request models in main.py")
else:
    print("Could not find old_models!")

# 2. Add /api/clubs/by-league endpoint
endpoint_code = """
@app.get("/api/clubs/by-league")
def api_get_clubs_by_league() -> dict[str, list[str]]:
    \"\"\"Returns real list of clubs grouped by league from SQLite database.\"\"\"
    import sqlite3
    db_path = Path("data/agency_desk.db")
    if not db_path.exists():
        db_path = Path("agency_desk.db")
    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT league, current_club FROM players WHERE current_club IS NOT NULL AND current_club != '' ORDER BY league, current_club")
    rows = cur.fetchall()
    conn.close()
    
    result: dict[str, list[str]] = {}
    for lg, clb in rows:
        if not lg or not clb:
            continue
        if lg not in result:
            result[lg] = []
        result[lg].append(clb)
    return result
"""

if "/api/clubs/by-league" not in content:
    # insert before @app.post("/api/agency/client/transfer-pipeline")
    target = '@app.post("/api/agency/client/transfer-pipeline")'
    content = content.replace(target, endpoint_code.strip() + "\n\n\n" + target)
    print("Added /api/clubs/by-league endpoint in main.py")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated src/sports_agency/api/main.py")
