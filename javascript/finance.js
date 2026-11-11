/**
 * AgencyOS Pro - Financial Calculator (EPL PSR & FIFA FFAR Caps)
 */

function calculatePsrStatus(currentLossGbp, transferFeeGbp, contractYears, weeklyWageGbp) {
  const annualAmortization = transferFeeGbp / Math.max(1, Math.min(5, contractYears));
  const annualWage = weeklyWageGbp * 52;
  const newThreeYearLoss = currentLossGbp + (annualAmortization * 3) + (annualWage * 3);
  const psrLimit = 105000000; // £105M limit for Premier League 3-year cycle
  const remainingHeadroom = psrLimit - newThreeYearLoss;

  return {
    isCompliant: newThreeYearLoss <= psrLimit,
    annualAmortization,
    annualWage,
    newThreeYearLoss,
    remainingHeadroom,
    headroomStatus: remainingHeadroom >= 0 ? '안전 (Safe)' : '규정 위반 (Risk)'
  };
}

function calculateFifaAgentFeeCap(annualRemunerationEur, isDualRepresentation = false) {
  const threshold = 200000; // $200,000 / €200,000 tier
  let feeCapPct = 0;
  if (annualRemunerationEur <= threshold) {
    feeCapPct = isDualRepresentation ? 10 : 5;
  } else {
    feeCapPct = isDualRepresentation ? 6 : 3;
  }
  const maxFeeEur = annualRemunerationEur * (feeCapPct / 100);
  return { feeCapPct, maxFeeEur };
}
