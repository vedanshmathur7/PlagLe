import { useState } from 'react';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [assignmentId, setAssignmentId] = useState('1');
  const [studentId, setStudentId] = useState('2');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setError('Please select a file to upload');
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
      setResult(data);
    } catch (err) {
      setError(err.message || 'Something went wrong during analysis');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <header className="header">
        <h1>PlagLe</h1>
        <p>Intelligent Plagiarism Detection System</p>
      </header>

      <main className="main-content">
        <section className="upload-section">
          <h2>Check Document</h2>
          <form onSubmit={handleSubmit} className="upload-form">
            <div className="form-group">
              <label htmlFor="file">Upload Document (.txt, .pdf, .docx)</label>
              <input 
                type="file" 
                id="file" 
                onChange={handleFileChange}
                accept=".txt,.pdf,.docx"
              />
            </div>
            <div className="form-row">
              <div className="form-group">
                <label htmlFor="assignmentId">Assignment ID</label>
                <input 
                  type="number" 
                  id="assignmentId" 
                  value={assignmentId} 
                  onChange={(e) => setAssignmentId(e.target.value)} 
                  required
                />
              </div>
              <div className="form-group">
                <label htmlFor="studentId">Student ID</label>
                <input 
                  type="number" 
                  id="studentId" 
                  value={studentId} 
                  onChange={(e) => setStudentId(e.target.value)} 
                  required
                />
              </div>
            </div>
            {error && <div className="error-message">{error}</div>}
            <button type="submit" disabled={loading || !file} className="submit-btn">
              {loading ? 'Analyzing...' : 'Run Plagiarism Check'}
            </button>
          </form>
        </section>

        {result && (
          <section className="results-section">
            <h2>Analysis Results</h2>
            <div className="result-card summary">
              <p><strong>Checked File:</strong> {result.document?.file_name}</p>
              <p><strong>Status:</strong> {result.success ? "Completed Successfully" : "Failed"}</p>
            </div>

            {result.plagiarism_check?.results?.length > 0 ? (
              <div className="findings">
                <h3>Similarities Detected</h3>
                {result.plagiarism_check.results.map((sim) => (
                  <div key={sim.similarity_id} className={`result-card ${sim.risk_level === 'High Risk' ? 'high-risk' : ''}`}>
                    <div className="sim-header">
                      <span className="risk-badge">{sim.risk_level}</span>
                      <span className="score-badge">{sim.score_percentage.toFixed(2)}% Match</span>
                    </div>
                    <p>Compared against <strong>{sim.doc2_name}</strong></p>
                    {result.reports?.find(r => r.similarity_id === sim.similarity_id) && (
                      <a 
                        href={`http://localhost:8000${result.reports.find(r => r.similarity_id === sim.similarity_id).report_url}`} 
                        className="download-btn"
                        target="_blank" rel="noreferrer"
                      >
                        Download PDF Report
                      </a>
                    )}
                  </div>
                ))}
              </div>
            ) : (
              <div className="no-findings">
                <p>✅ Looks good! No significant plagiarism detected.</p>
              </div>
            )}
          </section>
        )}
      </main>
    </div>
  );
}

export default App;
