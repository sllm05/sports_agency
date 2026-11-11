/**
 * AgencyOS Pro - Negotiation Sparring & Deal Memo Engine
 */

async function sendSparringMessage(conversationHistory, targetPlayer, userInput) {
  const payload = {
    history: conversationHistory,
    target: targetPlayer,
    message: userInput
  };
  const res = await fetch('/api/negotiation/sparring', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  if (!res.ok) throw new Error('협상 스파링 응답 오류');
  return await res.json();
}

async function signClientDealMemo(dealMemoData) {
  const res = await fetch('/api/agency/sign-contract', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(dealMemoData)
  });
  if (!res.ok) throw new Error('전속 계약 체결 실패');
  return await res.json();
}
