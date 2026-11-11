/**
 * AgencyOS Pro - Talent Scouting & DataMB Multi-Peer Matrix Engine
 */

let peerCompareList = [];
let peerCompareCategory = 'AUTO';
let peerMultiRadarInstance = null;
let peerIsManagerMode = false;

const PEER_PALETTE = [
  { border: '#ef4444', bg: 'rgba(239, 68, 68, 0.20)', name: 'Crimson Red' },
  { border: '#3b82f6', bg: 'rgba(59, 130, 246, 0.20)', name: 'Royal Blue' },
  { border: '#10b981', bg: 'rgba(16, 185, 129, 0.20)', name: 'Emerald Green' },
  { border: '#a855f7', bg: 'rgba(168, 85, 247, 0.20)', name: 'Purple' }
];

async function fetchScoutingPlayers(league = 'ALL', search = '') {
  const query = new URLSearchParams({ league, search });
  const res = await fetch(`/api/players?${query.toString()}`);
  if (!res.ok) throw new Error('선수 목록 조회 실패');
  return await res.json();
}

async function runDataMBPeerCompare(playerNames, category = 'AUTO', season = '25/26') {
  const res = await fetch('/api/scout/datamb-compare', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      player_names: playerNames,
      position_category: category,
      season: season
    })
  });
  if (!res.ok) throw new Error('DataMB 피어 비교 API 통신 오류');
  return await res.json();
}
