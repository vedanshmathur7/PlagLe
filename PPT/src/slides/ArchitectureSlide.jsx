import React from 'react'
import { Cable, CheckCircle2, Database, FileText, Globe2, Plug, RefreshCw, SatelliteDish, Server, ShieldCheck, Sigma, Workflow, Zap } from 'lucide-react'
import { MotionCard, Reveal, Stagger } from '../components/Motion.jsx'

const archBoxes = [
  { Icon: Workflow, title: 'React Frontend', port: 'Port 5173', tech: 'Vite + React 19' },
  { Icon: Server, title: 'FastAPI Backend', port: 'Port 8000', tech: 'Python + Uvicorn' },
  { Icon: Database, title: 'MySQL Database', port: 'Port 3306', tech: 'InnoDB Engine' },
]

const steps = [
  { n: 1, t: 'Upload Document', d: 'User uploads via React dashboard (PDF, DOCX, TXT)' },
  { n: 2, t: 'API Request', d: 'FastAPI receives file via multipart POST to /api/v1/check-plagiarism' },
  { n: 3, t: 'Validation', d: 'Extension whitelist + 10MB size limit, saved to disk' },
  { n: 4, t: 'Database Insert', d: 'Submission and Document records created in MySQL' },
  { n: 5, t: 'Text Processing', d: 'Extract text -> lowercase, remove punctuation & stopwords' },
  { n: 6, t: 'Similarity Compute', d: 'TF-IDF Vectorizer -> Cosine Similarity pairwise score' },
  { n: 7, t: 'Store Results', d: 'Scores above 15% threshold stored in Similarity table' },
  { n: 8, t: 'Report Generation', d: 'ReportLab generates PDF with risk classification', risks: true },
  { n: 9, t: 'API Response', d: 'JSON response with results + PDF download URLs' },
  { n: 10, t: 'Dashboard Render', d: 'Analytics cards, risk chart, paginated findings table' },
]

const backendFeatures = [
  { Icon: Plug, text: 'MySQL Connection Pooling (pool_size=10) for concurrency' },
  { Icon: ShieldCheck, text: 'Parameterized SQL queries - prevents SQL injection' },
  { Icon: RefreshCw, text: 'Context manager with auto commit/rollback' },
  { Icon: Globe2, text: 'CORS middleware for secure cross-origin comm' },
  { Icon: CheckCircle2, text: 'Pydantic schema validation on all models' },
  { Icon: FileText, text: 'Request logging middleware with timing' },
]

export default function ArchitectureSlide() {
  return (
    <>
      <Reveal className="section-header">
        <div className="section-badge">04 - Architecture</div>
        <h2 className="section-title">System Architecture & Data Flow</h2>
        <p className="section-subtitle">From upload to analytics dashboard</p>
      </Reveal>

      <Stagger className="arch-flow">
        {archBoxes.map((b, i) => (
          <React.Fragment key={i}>
            <MotionCard className="arch-box">
              <div className="arch-box-icon">
                <b.Icon className="h-7 w-7" aria-hidden="true" />
              </div>
              <div className="arch-box-title">{b.title}</div>
              <div className="arch-box-port">{b.port}</div>
              <div className="arch-box-tech">{b.tech}</div>
            </MotionCard>
            {i < 2 && <div className="arch-arrow">-&gt;</div>}
          </React.Fragment>
        ))}
      </Stagger>

      <Reveal>
        <h3 className="small-heading center flex items-center justify-center gap-3">
          <SatelliteDish className="h-5 w-5 text-indigo-200" aria-hidden="true" />
          Data Flow - 10 Steps
        </h3>
      </Reveal>
      <Stagger className="steps-grid">
        {steps.map((s) => (
          <MotionCard className="step-card" key={s.n}>
            <div className="step-num">{s.n}</div>
            <div className="step-content">
              <h4>{s.t}</h4>
              <p>{s.d}</p>
              {s.risks && (
                <div className="risk-badges">
                  <span className="risk-badge risk-low">Low 15-35%</span>
                  <span className="risk-badge risk-medium">Med 35-60%</span>
                  <span className="risk-badge risk-high">High 60-100%</span>
                </div>
              )}
            </div>
          </MotionCard>
        ))}
      </Stagger>

      <Reveal>
        <h3 className="small-heading center flex items-center justify-center gap-3">
          <Cable className="h-5 w-5 text-indigo-200" aria-hidden="true" />
          Key Backend Features
        </h3>
      </Reveal>
      <Stagger className="backend-grid">
        {backendFeatures.map((f, i) => (
          <MotionCard className="backend-item" key={i}>
            <span className="feature-icon">
              <f.Icon className="h-4 w-4" aria-hidden="true" />
            </span>
            <span>{f.text}</span>
          </MotionCard>
        ))}
      </Stagger>
    </>
  )
}
