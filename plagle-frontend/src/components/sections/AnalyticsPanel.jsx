import { createElement } from 'react';
import { BarChart3, FileCheck2, ShieldAlert, Waypoints } from 'lucide-react';
import { Card } from '../ui/Card';
import { EmptyState } from '../ui/EmptyState';
import { LoadingSkeleton } from '../ui/LoadingSkeleton';

const statCards = [
  { key: 'highestScore', label: 'Highest match', icon: ShieldAlert, suffix: '%' },
  { key: 'averageScore', label: 'Average overlap', icon: BarChart3, suffix: '%' },
  { key: 'reportCoverage', label: 'Report coverage', icon: FileCheck2, suffix: '%' },
  { key: 'integrityScore', label: 'Integrity score', icon: Waypoints, suffix: '%' },
];

export function AnalyticsPanel({ loading, result, metrics, checkedFile }) {
  return (
    <section id="analytics">
      <Card className="panel-card">
        <div className="section-heading">
          <div>
            <span className="section-kicker">Analytics Layer</span>
            <h3>Readable metrics and reviewer signals</h3>
          </div>
        </div>

        {loading ? (
          <div className="analytics-loading">
            <div className="stat-grid">
              {Array.from({ length: 4 }).map((_, index) => (
                <div key={index} className="stat-card">
                  <LoadingSkeleton className="skeleton-icon" />
                  <LoadingSkeleton className="skeleton-line skeleton-line-short" />
                  <LoadingSkeleton className="skeleton-line" />
                </div>
              ))}
            </div>
            <LoadingSkeleton className="chart-skeleton" />
          </div>
        ) : result ? (
          <>
            <div className="stat-grid">
              {statCards.map(({ key, label, icon: Icon, suffix }) => (
                <div key={key} className="stat-card">
                  <div className="stat-card-icon">{createElement(Icon, { size: 18 })}</div>
                  <span>{label}</span>
                  <strong>
                    {metrics[key].toFixed(2)}
                    {suffix}
                  </strong>
                </div>
              ))}
            </div>

            <div className="analytics-grid">
              <div className="chart-card">
                <div className="chart-header">
                  <div>
                    <span>Checked file</span>
                    <strong>{checkedFile || 'Current upload'}</strong>
                  </div>
                  <div className="chart-badge">{metrics.totalMatches} findings</div>
                </div>
                <div className="distribution-bars">
                  {metrics.scoreBands.map((band) => (
                    <div key={band.label} className="distribution-row">
                      <span>{band.label}</span>
                      <div className="distribution-track">
                        <div
                          className="distribution-fill"
                          style={{
                            width: `${metrics.totalMatches ? (band.value / metrics.totalMatches) * 100 : 4}%`,
                          }}
                        />
                      </div>
                      <strong>{band.value}</strong>
                    </div>
                  ))}
                </div>
              </div>

              <div className="chart-card">
                <div className="chart-header">
                  <div>
                    <span>Risk breakdown</span>
                    <strong>Where reviewers should focus</strong>
                  </div>
                </div>
                <div className="risk-stack">
                  {metrics.riskDistribution.map((item) => (
                    <div key={item.label} className="risk-stack-row">
                      <div className="risk-stack-copy">
                        <span>{item.label}</span>
                        <strong>{item.count}</strong>
                      </div>
                      <div className="risk-stack-track">
                        <div
                          className={`risk-stack-fill risk-stack-fill-${item.tone}`}
                          style={{
                            width: `${metrics.totalMatches ? (item.count / metrics.totalMatches) * 100 : 6}%`,
                          }}
                        />
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </>
        ) : (
          <EmptyState
            badge="Awaiting data"
            title="Analytics will populate after the first scan"
            description="The dashboard is ready for charts, risk distribution, and integrity metrics as soon as a document is analyzed."
          />
        )}
      </Card>
    </section>
  );
}
