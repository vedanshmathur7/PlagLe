import { startTransition, useDeferredValue, useEffect, useMemo, useState } from 'react';
import { FileDown } from 'lucide-react';
import './App.css';
import { Sidebar } from './components/layout/Sidebar';
import { Topbar } from './components/layout/Topbar';
import { AnalyticsPanel } from './components/sections/AnalyticsPanel';
import { FindingsTable } from './components/sections/FindingsTable';
import { HeroSection } from './components/sections/HeroSection';
import { SubmissionPanel } from './components/sections/SubmissionPanel';
import { Modal } from './components/ui/Modal';
import { ToastStack } from './components/ui/ToastStack';
import { buildFindings, deriveDashboardMetrics, getRiskTone } from './utils/dashboard';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';
const PAGE_SIZE = 5;

const getInitialTheme = () => {
  if (typeof window === 'undefined') {
    return 'dark';
  }

  const storedTheme = window.localStorage.getItem('plagle-theme');

  if (storedTheme === 'light' || storedTheme === 'dark') {
    return storedTheme;
  }

  return window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark';
};

function App() {
  const [theme, setTheme] = useState(getInitialTheme);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [file, setFile] = useState(null);
  const [assignmentId, setAssignmentId] = useState('1');
  const [studentId, setStudentId] = useState('5');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  const [riskFilter, setRiskFilter] = useState('all');
  const [sortKey, setSortKey] = useState('score');
  const [sortDirection, setSortDirection] = useState('desc');
  const [currentPage, setCurrentPage] = useState(1);
  const [selectedFinding, setSelectedFinding] = useState(null);
  const [toasts, setToasts] = useState([]);

  const deferredSearch = useDeferredValue(searchTerm);
  const reportBaseUrl = API_URL.replace(/\/api\/v1\/?$/, '');

  useEffect(() => {
    document.documentElement.dataset.theme = theme;
    window.localStorage.setItem('plagle-theme', theme);
  }, [theme]);

  const findings = useMemo(() => buildFindings(result), [result]);
  const metrics = useMemo(() => deriveDashboardMetrics(findings), [findings]);

  const filteredFindings = useMemo(() => {
    const normalizedQuery = deferredSearch.trim().toLowerCase();
    const sorted = [...findings]
      .filter((item) => {
        const matchesQuery =
          !normalizedQuery ||
          item.doc2_name.toLowerCase().includes(normalizedQuery) ||
          item.risk_level.toLowerCase().includes(normalizedQuery);
        const matchesRisk = riskFilter === 'all' || item.tone === riskFilter;

        return matchesQuery && matchesRisk;
      })
      .sort((left, right) => {
        const direction = sortDirection === 'asc' ? 1 : -1;

        if (sortKey === 'document') {
          return left.doc2_name.localeCompare(right.doc2_name) * direction;
        }

        if (sortKey === 'risk') {
          const rank = { safe: 1, warning: 2, danger: 3 };
          return (rank[left.tone] - rank[right.tone]) * direction;
        }

        if (sortKey === 'report') {
          return ((left.report ? 1 : 0) - (right.report ? 1 : 0)) * direction;
        }

        return ((left.score_percentage ?? 0) - (right.score_percentage ?? 0)) * direction;
      });

    return sorted;
  }, [deferredSearch, findings, riskFilter, sortDirection, sortKey]);

  const totalPages = Math.max(1, Math.ceil(filteredFindings.length / PAGE_SIZE));
  const paginatedFindings = filteredFindings.slice(
    (currentPage - 1) * PAGE_SIZE,
    currentPage * PAGE_SIZE,
  );

  useEffect(() => {
    setCurrentPage(1);
  }, [deferredSearch, riskFilter, sortDirection, sortKey]);

  useEffect(() => {
    if (currentPage > totalPages) {
      setCurrentPage(totalPages);
    }
  }, [currentPage, totalPages]);

  const dismissToast = (id) => {
    setToasts((currentToasts) => currentToasts.filter((toast) => toast.id !== id));
  };

  const showToast = (title, description, tone = 'info') => {
    const id = `${Date.now()}-${Math.random().toString(16).slice(2)}`;
    setToasts((currentToasts) => [...currentToasts, { id, title, description, tone }]);
    window.setTimeout(() => dismissToast(id), 4200);
  };

  const handleFileChange = (nextFile) => {
    setFile(nextFile);
    if (nextFile) {
      setError('');
    }
  };

  const handleSortChange = (nextKey) => {
    if (sortKey === nextKey) {
      setSortDirection((currentDirection) => (currentDirection === 'asc' ? 'desc' : 'asc'));
      return;
    }

    setSortKey(nextKey);
    setSortDirection(nextKey === 'document' ? 'asc' : 'desc');
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!file) {
      const message = 'Please select a document before starting the scan.';
      setError(message);
      showToast('Document required', message, 'error');
      return;
    }

    setLoading(true);
    setError('');
    setResult(null);

    const formData = new FormData();
    formData.append('file', file);
    formData.append('assignment_id', assignmentId);
    formData.append('student_id', studentId);
    formData.append('generated_by', '1');
    formData.append('algorithm_id', '1');

    try {
      const response = await fetch(`${API_URL}/check-plagiarism`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Error: ${response.statusText}`);
      }

      const data = await response.json();

      startTransition(() => {
        setResult(data);
        setSelectedFinding(null);
      });

      showToast(
        'Analysis complete',
        data.plagiarism_check?.results?.length
          ? 'Similarity findings are ready for review.'
          : 'No significant plagiarism was detected.',
        'success',
      );
    } catch (err) {
      const message = err.message || 'Something went wrong during analysis.';
      setError(message);
      showToast('Analysis failed', message, 'error');
    } finally {
      setLoading(false);
    }
  };

  const highlightedFinding = selectedFinding
    ? {
        ...selectedFinding,
        recommendation:
          getRiskTone(selectedFinding.risk_level) === 'danger'
            ? 'Prioritize manual review and compare the generated PDF evidence before grading.'
            : 'Review the similarity context and validate whether overlap is expected or cited.',
      }
    : null;

  return (
    <div className="dashboard-shell">
      <div className="background-orb background-orb-one" />
      <div className="background-orb background-orb-two" />

      <Sidebar
        collapsed={sidebarCollapsed}
        onToggle={() => setSidebarCollapsed((currentValue) => !currentValue)}
        metrics={metrics}
        hasResult={Boolean(result)}
      />

      <div className={`dashboard-main ${sidebarCollapsed ? 'dashboard-main-expanded' : ''}`}>
        <Topbar
          theme={theme}
          onToggleTheme={() => setTheme((currentTheme) => (currentTheme === 'dark' ? 'light' : 'dark'))}
          onToggleSidebar={() => setSidebarCollapsed((currentValue) => !currentValue)}
          sidebarCollapsed={sidebarCollapsed}
          activeFile={file?.name}
          totalFindings={metrics.totalMatches}
        />

        <main className="dashboard-content">
          <HeroSection file={file} metrics={metrics} loading={loading} />

          <div className="content-grid">
            <SubmissionPanel
              file={file}
              assignmentId={assignmentId}
              studentId={studentId}
              loading={loading}
              error={error}
              onFileChange={handleFileChange}
              onAssignmentChange={setAssignmentId}
              onStudentChange={setStudentId}
              onSubmit={handleSubmit}
            />

            <AnalyticsPanel
              loading={loading}
              result={result}
              metrics={metrics}
              checkedFile={result?.document?.file_name || file?.name}
            />
          </div>

          <FindingsTable
            loading={loading}
            result={result}
            findings={paginatedFindings}
            totalFindings={filteredFindings.length}
            searchTerm={searchTerm}
            onSearchChange={setSearchTerm}
            riskFilter={riskFilter}
            onRiskFilterChange={setRiskFilter}
            sortKey={sortKey}
            sortDirection={sortDirection}
            onSortChange={handleSortChange}
            currentPage={currentPage}
            totalPages={totalPages}
            onPageChange={setCurrentPage}
            onSelectFinding={setSelectedFinding}
            reportBaseUrl={reportBaseUrl}
          />
        </main>
      </div>

      <ToastStack toasts={toasts} onDismiss={dismissToast} />

      <Modal
        open={Boolean(highlightedFinding)}
        title={highlightedFinding?.doc2_name}
        subtitle={highlightedFinding ? `${highlightedFinding.risk_level} • ${highlightedFinding.score_percentage.toFixed(2)}% match` : ''}
        onClose={() => setSelectedFinding(null)}
      >
        {highlightedFinding && (
          <div className="modal-content-stack">
            <div className="detail-grid">
              <div className="detail-card">
                <span>Compared document</span>
                <strong>{highlightedFinding.doc2_name}</strong>
              </div>
              <div className="detail-card">
                <span>Similarity intensity</span>
                <strong>{highlightedFinding.score_percentage.toFixed(2)}%</strong>
              </div>
            </div>

            <div className="modal-note">
              <h4>Reviewer recommendation</h4>
              <p>{highlightedFinding.recommendation}</p>
            </div>

            <div className="modal-actions">
              {highlightedFinding.report && (
                <a
                  href={`${reportBaseUrl}${highlightedFinding.report.report_url}`}
                  className="button button-primary"
                  target="_blank"
                  rel="noreferrer"
                >
                  <FileDown size={18} />
                  Download PDF Report
                </a>
              )}
              <a href="#scan" className="button button-secondary" onClick={() => setSelectedFinding(null)}>
                Start another scan
              </a>
            </div>
          </div>
        )}
      </Modal>
    </div>
  );
}

export default App;
