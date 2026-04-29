import { FileUp, LoaderCircle } from 'lucide-react';
import { Button } from '../ui/Button';
import { Card } from '../ui/Card';
import { FloatingInput } from '../ui/FloatingInput';

export function SubmissionPanel({
  file,
  assignmentId,
  studentId,
  loading,
  error,
  onFileChange,
  onAssignmentChange,
  onStudentChange,
  onSubmit,
}) {
  return (
    <section id="scan">
      <Card className="panel-card">
        <div className="section-heading">
          <div>
            <span className="section-kicker">Submission Console</span>
            <h3>Launch a new plagiarism scan</h3>
          </div>
          <div className={`status-pill ${loading ? 'status-pill-live' : ''}`}>
            {loading ? 'Analyzing now' : 'Ready'}
          </div>
        </div>

        <form className="submission-form" onSubmit={onSubmit}>
          <label className={`upload-dropzone ${file ? 'upload-dropzone-active' : ''}`} htmlFor="file">
            <input
              id="file"
              type="file"
              accept=".txt,.pdf,.docx"
              onChange={(event) => onFileChange(event.target.files?.[0] ?? null)}
            />
            <div className="upload-dropzone-icon">
              <FileUp size={22} />
            </div>
            <strong>{file ? file.name : 'Drop or choose a document'}</strong>
            <p>
              Support for TXT, PDF, and DOCX. The current backend workflow remains unchanged.
            </p>
          </label>

          <div className="floating-grid">
            <FloatingInput
              id="assignmentId"
              label="Assignment ID"
              type="number"
              min="1"
              value={assignmentId}
              onChange={onAssignmentChange}
              required
            />
            <FloatingInput
              id="studentId"
              label="Student ID"
              type="number"
              min="1"
              value={studentId}
              onChange={onStudentChange}
              required
            />
          </div>

          {error && <div className="message message-error">{error}</div>}

          <div className="form-footer">
            <div className="form-helper-copy">
              <span>Validation</span>
              <p>Reviewer-friendly states, cleaner spacing, same API contract.</p>
            </div>
            <Button type="submit" disabled={loading || !file}>
              {loading ? (
                <>
                  <LoaderCircle size={16} className="spin" />
                  Running scan
                </>
              ) : (
                'Run plagiarism analysis'
              )}
            </Button>
          </div>
        </form>
      </Card>
    </section>
  );
}
