import { ArrowDownUp, ChevronLeft, ChevronRight, Eye, FileDown, Search } from 'lucide-react';
import { Button } from '../ui/Button';
import { Card } from '../ui/Card';
import { EmptyState } from '../ui/EmptyState';
import { LoadingSkeleton } from '../ui/LoadingSkeleton';

const columns = [
  { key: 'document', label: 'Document' },
  { key: 'risk', label: 'Risk level' },
  { key: 'score', label: 'Similarity' },
  { key: 'report', label: 'Report' },
];

export function FindingsTable({
  loading,
  result,
  findings,
  totalFindings,
  searchTerm,
  onSearchChange,
  riskFilter,
  onRiskFilterChange,
  sortKey,
  sortDirection,
  onSortChange,
  currentPage,
  totalPages,
  onPageChange,
  onSelectFinding,
  reportBaseUrl,
}) {
  return (
    <section id="findings">
      <Card className="panel-card findings-panel">
        <div className="section-heading">
          <div>
            <span className="section-kicker">Findings Workspace</span>
            <h3>Filter, sort, and inspect results with less friction</h3>
          </div>
        </div>

        {loading ? (
          <div className="table-skeleton">
            <LoadingSkeleton className="skeleton-line" />
            <LoadingSkeleton className="skeleton-line" />
            <LoadingSkeleton className="skeleton-block" />
          </div>
        ) : !result ? (
          <EmptyState
            badge="No findings yet"
            title="Run a scan to unlock the review table"
            description="The table layer adds search, sorting, pagination, and quick access to evidence reports."
          />
        ) : totalFindings === 0 ? (
          <EmptyState
            badge="Clear result"
            title="No significant plagiarism detected"
            description="This submission did not return notable overlaps after the current filter set and scan results were applied."
          />
        ) : (
          <>
            <div className="table-toolbar">
              <label className="search-field">
                <Search size={16} />
                <input
                  type="search"
                  value={searchTerm}
                  onChange={(event) => onSearchChange(event.target.value)}
                  placeholder="Search document or risk level"
                />
              </label>

              <label className="select-field">
                <span>Risk filter</span>
                <select value={riskFilter} onChange={(event) => onRiskFilterChange(event.target.value)}>
                  <option value="all">All</option>
                  <option value="danger">High risk</option>
                  <option value="warning">Medium risk</option>
                  <option value="low">Low risk</option>
                </select>
              </label>
            </div>

            <div className="table-shell">
              <table className="findings-table">
                <thead>
                  <tr>
                    {columns.map((column) => (
                      <th key={column.key}>
                        <button type="button" className="table-sort" onClick={() => onSortChange(column.key)}>
                          <span>{column.label}</span>
                          <ArrowDownUp size={14} className={sortKey === column.key ? 'table-sort-active' : ''} />
                          {sortKey === column.key && <em>{sortDirection}</em>}
                        </button>
                      </th>
                    ))}
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {findings.map((finding) => (
                    <tr key={finding.similarity_id}>
                      <td>
                        <div className="document-cell">
                          <strong>{finding.doc2_name}</strong>
                          <span>Match #{finding.order}</span>
                        </div>
                      </td>
                      <td>
                        <span className={`risk-pill risk-pill-${finding.tone}`}>{finding.risk_level}</span>
                      </td>
                      <td>
                        <div className="score-cell">
                          <strong>{finding.score_percentage.toFixed(2)}%</strong>
                          <div className="mini-track">
                            <div
                              className={`mini-track-fill mini-track-fill-${finding.tone}`}
                              style={{ width: `${Math.min(finding.score_percentage, 100)}%` }}
                            />
                          </div>
                        </div>
                      </td>
                      <td>{finding.report ? 'Available' : 'Pending'}</td>
                      <td>
                        <div className="table-actions">
                          <button type="button" className="icon-button" onClick={() => onSelectFinding(finding)} aria-label="Open finding details">
                            <Eye size={16} />
                          </button>
                          {finding.report && (
                            <a
                              className="button button-secondary button-sm"
                              href={`${reportBaseUrl}${finding.report.report_url}`}
                              target="_blank"
                              rel="noreferrer"
                              title="Download PDF report"
                            >
                              <FileDown size={14} />
                              <span>Report</span>
                            </a>
                          )}
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <div className="pagination-row">
              <p>
                Showing {(currentPage - 1) * 5 + 1}-
                {Math.min(currentPage * 5, totalFindings)} of {totalFindings} findings
              </p>
              <div className="pagination-actions">
                <Button
                  variant="secondary"
                  size="sm"
                  onClick={() => onPageChange(Math.max(1, currentPage - 1))}
                  disabled={currentPage === 1}
                >
                  <ChevronLeft size={16} />
                  Prev
                </Button>
                <span className="pagination-indicator">
                  Page {currentPage} / {totalPages}
                </span>
                <Button
                  variant="secondary"
                  size="sm"
                  onClick={() => onPageChange(Math.min(totalPages, currentPage + 1))}
                  disabled={currentPage === totalPages}
                >
                  Next
                  <ChevronRight size={16} />
                </Button>
              </div>
            </div>
          </>
        )}
      </Card>
    </section>
  );
}
