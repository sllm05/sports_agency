def fix_render_analysis(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    old_fn = """    function renderAnalysisAndSparring(data) {
      const st = data.state || {};
      document.getElementById('analysis-section').classList.remove('hidden');
      const tid = data.thread_id ? String(data.thread_id) : 'deal_init';
      document.getElementById('thread-badge').textContent = `ID: ${tid.slice(0, 8)}`;"""

    new_fn = """    function renderAnalysisAndSparring(data) {
      if (!data) return;
      const st = data.state || {};
      const analysisSec = document.getElementById('analysis-section');
      if (analysisSec) analysisSec.classList.remove('hidden');
      const tid = data.thread_id ? String(data.thread_id) : 'deal_init';
      const threadBadge = document.getElementById('thread-badge');
      if (threadBadge) threadBadge.textContent = `ID: ${tid ? tid.slice(0, 8) : ''}`;"""

    if old_fn in content:
        content = content.replace(old_fn, new_fn)
        print(f"Guarded renderAnalysisAndSparring head in {filepath}")

    old_tail = """      renderSparringTranscript(st.sparring_transcript || []);
      document.getElementById('analysis-section').scrollIntoView({ behavior: 'smooth' });
    }

    function renderSparringTranscript(transcript) {
      const box = document.getElementById('sparring-chat-box');
      box.innerHTML = transcript.map(item => {"""

    new_tail = """      renderSparringTranscript(st.sparring_transcript || []);
      const analysisSecEl = document.getElementById('analysis-section');
      if (analysisSecEl) analysisSecEl.scrollIntoView({ behavior: 'smooth' });
    }

    function renderSparringTranscript(transcript) {
      const box = document.getElementById('sparring-chat-box');
      if (!box) return;
      box.innerHTML = transcript.map(item => {"""

    if old_tail in content:
        content = content.replace(old_tail, new_tail)
        print(f"Guarded renderSparringTranscript in {filepath}")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_render_analysis('src/sports_agency/api/static/index.html')
fix_render_analysis('html/index.html')
