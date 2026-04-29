export const defaultInsights = [
  { label: 'Detection engine', value: 'Hybrid semantic scan' },
  { label: 'Best for', value: 'Assignments, labs, essays' },
  { label: 'Output', value: 'Risk score + PDF evidence' },
];

export const navigationItems = [
  { id: 'overview', label: 'Overview' },
  { id: 'scan', label: 'Scan' },
  { id: 'analytics', label: 'Analytics' },
  { id: 'findings', label: 'Findings' },
];

// Risk tiers (aligned with backend classify_risk thresholds):
//   Low Risk    → 15–35%  score  → tone: 'low'
//   Medium Risk → 35–60%  score  → tone: 'warning'
//   High Risk   → 60–100% score  → tone: 'danger'
//   (Below 15% never surfaces — filtered by SIMILARITY_THRESHOLD)
export const getRiskTone = (riskLevel = '') => {
  const normalized = riskLevel.toLowerCase();

  if (normalized.includes('high')) return 'danger';
  if (normalized.includes('medium')) return 'warning';
  if (normalized.includes('low')) return 'low';

  return 'safe';
};

export const buildFindings = (result) => {
  const reports = result?.reports ?? [];
  const findings = result?.plagiarism_check?.results ?? [];

  return findings.map((finding, index) => ({
    ...finding,
    order: index + 1,
    tone: getRiskTone(finding.risk_level),
    report: reports.find((item) => item.similarity_id === finding.similarity_id) ?? null,
  }));
};

export const deriveDashboardMetrics = (findings) => {
  const totalMatches = findings.length;
  const highestScore = totalMatches ? Math.max(...findings.map((item) => item.score_percentage ?? 0)) : 0;
  const averageScore = totalMatches
    ? findings.reduce((sum, item) => sum + (item.score_percentage ?? 0), 0) / totalMatches
    : 0;
  const highRiskCount = findings.filter((item) => item.tone === 'danger').length;
  const reportCoverage = totalMatches
    ? Math.round((findings.filter((item) => item.report).length / totalMatches) * 100)
    : 0;

  const riskDistribution = [
    {
      label: 'High risk',
      tone: 'danger',
      count: findings.filter((item) => item.tone === 'danger').length,
    },
    {
      label: 'Medium risk',
      tone: 'warning',
      count: findings.filter((item) => item.tone === 'warning').length,
    },
    {
      label: 'Low risk',
      tone: 'low',
      count: findings.filter((item) => item.tone === 'low').length,
    },
  ];

  const scoreBands = [
    { label: '0-25', value: findings.filter((item) => item.score_percentage < 25).length },
    {
      label: '25-50',
      value: findings.filter((item) => item.score_percentage >= 25 && item.score_percentage < 50).length,
    },
    {
      label: '50-75',
      value: findings.filter((item) => item.score_percentage >= 50 && item.score_percentage < 75).length,
    },
    { label: '75-100', value: findings.filter((item) => item.score_percentage >= 75).length },
  ];

  return {
    totalMatches,
    highestScore,
    averageScore,
    highRiskCount,
    reportCoverage,
    integrityScore: Math.max(0, 100 - averageScore),
    riskDistribution,
    scoreBands,
  };
};
