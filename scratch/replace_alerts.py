import re

def clean_alerts(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replacement mappings or regex
    # Replace alert with showToast based on content context
    def replace_alert(match):
        inner = match.group(1).strip()
        # determine type
        lower_inner = inner.lower()
        if any(w in lower_inner for w in ['오류', '실패', 'err', 'error', 'fail', '없습니다']):
            return f"showToast({inner}, 'error')"
        elif any(w in lower_inner for w in ['완료', '성공', '환영', '체결', '승인', '복사', '등록']):
            return f"showToast({inner}, 'success')"
        elif any(w in lower_inner for w in ['선택', '입력', '주의', '로그인']):
            return f"showToast({inner}, 'warning')"
        else:
            return f"showToast({inner}, 'info')"

    # Pattern for alert(...) but not inside comments or strings
    new_content = re.sub(r'\balert\((.*?)\);', lambda m: replace_alert(m) + ';', content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Updated {filepath}")

clean_alerts('src/sports_agency/api/static/index.html')
clean_alerts('html/index.html')
