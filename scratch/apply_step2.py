with open('src/sports_agency/api/static/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

start_marker = 'async function startTransferPipelineEvaluation(e) {'
end_marker = 'async function submitClientTransfer(e) {'

i1 = text.find(start_marker)
i2 = text.find(end_marker)
assert i1 != -1 and i2 != -1, f'Markers not found: i1={i1}, i2={i2}'

with open('scratch/patch_html_js.py', 'r', encoding='utf-8') as f:
    pjs = f.read()

code_start = pjs.find('new_transfer_pipeline_code = """') + len('new_transfer_pipeline_code = """')
code_end = pjs.find('"""\n\nif old_start_transfer_func.search(content):')
new_code = pjs[code_start:code_end] + '\n\n    '

new_text = text[:i1] + new_code + text[i2:]
with open('src/sports_agency/api/static/index.html', 'w', encoding='utf-8') as f:
    f.write(new_text)

print('Successfully applied Step 2 to index.html! New length:', len(new_text))
