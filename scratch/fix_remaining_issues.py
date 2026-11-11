def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. contract_expires slice fix
    old_slice = "${p.contract_expires.slice(0,4)}만료"
    new_slice = "${(p.contract_expires ? String(p.contract_expires) : '2027').slice(0,4)}만료"
    if old_slice in content:
        content = content.replace(old_slice, new_slice)
        print(f"Fixed contract_expires.slice in {filepath}")
    else:
        print(f"contract_expires.slice already fixed in {filepath}")

    # 2. eliminate confirm calls
    old_c1 = "if (!confirm(`[${email}] 직원의 가입을 승인하시겠습니까?`)) return;"
    new_c1 = "// Direct approval without popup"
    if old_c1 in content:
        content = content.replace(old_c1, new_c1)
        print(f"Fixed confirm 1 (approvePendingUser) in {filepath}")

    old_c2 = "if (!confirm(`'${targetName}' 님을 영입 관심 리스트에서 제외하시겠습니까?`)) return;"
    new_c2 = "// Direct remove without popup"
    if old_c2 in content:
        content = content.replace(old_c2, new_c2)
        print(f"Fixed confirm 2 (removeTargetFromWatchlist) in {filepath}")

    old_c3 = """      if (commissionPct > 5.0) {
        const confirmHigh = confirm(`[FIFA FFAR 규정 권고 안내]\\n현재 입력하신 수수료율(${commissionPct}%)은 FIFA 권고 상한(3~5%)을 상회합니다.\\n사내 법무팀 특별 승인 하에 체결을 진행하시겠습니까?`);
        if (!confirmHigh) return;
      }"""
    new_c3 = """      if (commissionPct > 5.0) {
        showToast('[FIFA FFAR 규정 안내] 법정 권고 상한(5%)을 초과하여 사내 특별 승인 조항이 적용됩니다.', 'warning', 4000);
      }"""
    if old_c3 in content:
        content = content.replace(old_c3, new_c3)
        print(f"Fixed confirm 3 (dealmemo signoff) in {filepath}")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Saved {filepath}")

fix_file('src/sports_agency/api/static/index.html')
fix_file('html/index.html')
