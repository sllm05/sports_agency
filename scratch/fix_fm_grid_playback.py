from pathlib import Path

file_path = Path("rea/fm_2d_grid_match.html")
content = file_path.read_text(encoding="utf-8")

old_on_select = """    function onSelectPlayer(playerId) {
      const p = PLAYERS_DATABASE.find(item => item.player_id == playerId);
      if (!p) return;
      currentPlayer = p;
      currentActionIdx = 0;
      currentTime = 0;

      // 프로필 카드 업데이트
      document.getElementById('pAvatar').innerText = (p.name_ko || p.name).slice(0, 1);
      document.getElementById('pNameKo').innerText = p.name_ko || p.name;
      document.getElementById('pClub').innerText = `${p.current_club || ''} · ${p.league || ''}`;
      document.getElementById('pPosBadge').innerText = p.position || 'ST';
      document.getElementById('pArchetype').innerText = p.tactical_archetype || '전술적 특화 플레이어';

      const valM = (p.market_value_eur / 1000000).toFixed(0);
      document.getElementById('pMarketVal').innerText = `€${valM}M (약 ${Math.round(valM * 14.8)}억 원)`;

      document.getElementById('pStatXg').innerText = `${p.xg_per90 ? p.xg_per90.toFixed(2) : '-'} (실득점 ${p.goals_per90 ? p.goals_per90.toFixed(2) : '-'})`;
      document.getElementById('pStatKp').innerText = `${p.key_passes_per90 ? p.key_passes_per90.toFixed(1) : '-'}회/90`;
      document.getElementById('pStatProg').innerText = `${p.progressive_actions_per90 ? p.progressive_actions_per90.toFixed(1) : '-'}회/90`;
      document.getElementById('pStatDef').innerText = `${p.defensive_duels_won_pct ? p.defensive_duels_won_pct.toFixed(0) : '-'}%`;
      document.getElementById('pStatPctl').innerText = `상위 ${(100 - (p.pos_percentile || 50))}%`;

      // 유튜브 링크 설정
      const ytId = YT_MAP[p.name_ko] || YT_MAP[p.name] || 'YhEcyglkOx0';
      document.getElementById('btnYtHighlight').onclick = () => {
        window.open(`https://www.youtube.com/watch?v=${ytId}`, '_blank');
      };

      // 액션 버튼 목록 생성
      const actions = generatePlayerActions(p);
      const listContainer = document.getElementById('actionList');
      listContainer.innerHTML = '';

      actions.forEach((act, idx) => {
        const div = document.createElement('div');
        div.className = `action-card ${idx === 0 ? 'active' : ''}`;
        div.onclick = () => {
          currentActionIdx = idx;
          currentTime = 0;
          document.querySelectorAll('.action-card').forEach((c, i) => {
            c.className = `action-card ${i === idx ? 'active' : ''}`;
          });
        };
        div.innerHTML = `
          <span class="act-tag ${act.tag}">${act.tagText}</span>
          <div class="act-title">${act.title}</div>
          <div class="act-desc">${act.desc}</div>
        `;
        listContainer.appendChild(div);
      });

      renderPitch();
    }"""

new_on_select = """    function onSelectPlayer(playerId) {
      const p = PLAYERS_DATABASE.find(item => item.player_id == playerId);
      if (!p) return;
      currentPlayer = p;
      currentActionIdx = 0;
      currentTime = 0;

      // 프로필 카드 안전한 업데이트 (실제 HTML ID 매핑)
      const nameEl = document.getElementById('pCardName');
      if (nameEl) nameEl.innerText = p.name_ko || p.name;

      const posEl = document.getElementById('pCardPos');
      if (posEl) posEl.innerText = p.position || 'ST';

      const clubEl = document.getElementById('pCardClub');
      const valM = (p.market_value_eur / 1000000).toFixed(0);
      if (clubEl) clubEl.innerText = `${p.current_club || ''} · ${p.league || ''} · €${valM}M (약 ${Math.round(valM * 14.8)}억 원)`;

      const archEl = document.getElementById('pCardArchetype');
      if (archEl) archEl.innerText = p.tactical_archetype || '전술 특화 플레이어';

      const strEl = document.getElementById('pCardStrengths');
      if (strEl) strEl.innerText = `핵심 강점: ${p.strengths_tags || '골 결정력, 전술적 침투'}`;

      const goalsEl = document.getElementById('pStatGoals');
      if (goalsEl) goalsEl.innerText = `${p.goals_per90 ? p.goals_per90.toFixed(2) : '-'} 골/90`;

      const xgEl = document.getElementById('pStatXg');
      if (xgEl) xgEl.innerText = `${p.xg_per90 ? p.xg_per90.toFixed(2) : '-'} (전환율: ${p.finishing_clinicality || '보통'})`;

      const kpEl = document.getElementById('pStatKp');
      if (kpEl) kpEl.innerText = `${p.key_passes_per90 ? p.key_passes_per90.toFixed(1) : '-'} 회/90`;

      const progEl = document.getElementById('pStatProg');
      if (progEl) progEl.innerText = `${p.progressive_actions_per90 ? p.progressive_actions_per90.toFixed(1) : '-'} 회/90`;

      const defEl = document.getElementById('pStatDef');
      if (defEl) defEl.innerText = `${p.defensive_duels_won_pct ? p.defensive_duels_won_pct.toFixed(0) : '-'} %`;

      const pctlEl = document.getElementById('pStatPctl');
      if (pctlEl) pctlEl.innerText = `상위 ${(100 - (p.pos_percentile || 50))}%`;

      // 공식 유튜브 하이라이트 동기화
      const ytId = YT_MAP[p.name_ko] || YT_MAP[p.name] || 'YhEcyglkOx0';
      const ytBtn = document.getElementById('ytSyncBtn');
      if (ytBtn) {
        ytBtn.href = `https://www.youtube.com/watch?v=${ytId}`;
        ytBtn.onclick = (e) => {
          e.preventDefault();
          window.open(`https://www.youtube.com/watch?v=${ytId}`, '_blank');
        };
      }

      // 액션 버튼 목록 생성
      const actions = generatePlayerActions(p);
      const listContainer = document.getElementById('actionList');
      if (listContainer) {
        listContainer.innerHTML = '';
        actions.forEach((act, idx) => {
          const div = document.createElement('div');
          div.className = `action-card ${idx === 0 ? 'active' : ''}`;
          div.onclick = () => {
            currentActionIdx = idx;
            currentTime = 0;
            document.querySelectorAll('.action-card').forEach((c, i) => {
              c.className = `action-card ${i === idx ? 'active' : ''}`;
            });
            renderPitch();
          };
          div.innerHTML = `
            <span class="act-tag ${act.tag}">${act.tagText}</span>
            <div class="act-title">${act.title}</div>
            <div class="act-desc">${act.desc}</div>
          `;
          listContainer.appendChild(div);
        });
      }

      renderPitch();
    }"""

assert old_on_select in content, "old_on_select not found"
content = content.replace(old_on_select, new_on_select, 1)

# Also update HUD updates in renderPitch with null safety
old_hud = """      // HUD 업데이트
      const phase = state.currentPhase;
      const heroRole = currentPlayer.position ? `[${currentPlayer.name_ko || currentPlayer.name} · ${currentPlayer.position}] ` : '';
      document.getElementById('hudActionText').innerText = heroRole + (phase.status || action.title);
      document.getElementById('hudMetricText').innerText = phase.metric || `진행: ${currentTime.toFixed(1)}s`;
      document.getElementById('timeLabel').innerText = `${currentTime.toFixed(1)}s / ${TOTAL_DURATION.toFixed(1)}s`;
      document.getElementById('timeSlider').value = currentTime;"""

new_hud = """      // HUD 업데이트 (안전한 null 체크)
      const phase = state.currentPhase || {};
      const heroRole = currentPlayer.position ? `[${currentPlayer.name_ko || currentPlayer.name} · ${currentPlayer.position}] ` : '';
      
      const hudAction = document.getElementById('hudActionText');
      if (hudAction) hudAction.innerText = heroRole + (phase.status || action.title);

      const hudMetric = document.getElementById('hudMetricText');
      if (hudMetric) hudMetric.innerText = phase.metric || `진행: ${currentTime.toFixed(1)}s`;

      const hudPhaseTag = document.getElementById('hudPhaseTag');
      if (hudPhaseTag) hudPhaseTag.innerText = action.tagText || '전술 전개';

      const timeLbl = document.getElementById('timeLabel');
      if (timeLbl) timeLbl.innerText = `${currentTime.toFixed(1)}s / ${TOTAL_DURATION.toFixed(1)}s`;

      const timeSld = document.getElementById('timeSlider');
      if (timeSld) timeSld.value = currentTime;"""

assert old_hud in content, "old_hud not found"
content = content.replace(old_hud, new_hud, 1)

file_path.write_text(content, encoding="utf-8")
print("Fixed onSelectPlayer and renderPitch in rea/fm_2d_grid_match.html successfully!")
