import React from 'react'
import {
  BarChart3,
  Braces,
  Building2,
  Database,
  FileCode2,
  Flag,
  Layers3,
  Network,
  RefreshCw,
  Server,
  Sparkles,
  UploadCloud,
  Workflow,
  Zap,
} from 'lucide-react'
import { MotionCard, Reveal, Stagger } from '../components/Motion.jsx'

const features = [
  [Building2, 'A full-stack plagiarism detection platform designed for academic institutions'],
  [UploadCloud, 'Instructors upload student submissions (PDF, DOCX, TXT)'],
  [RefreshCw, 'System automatically compares every document pair within the same assignment'],
  [Sparkles, 'Generates similarity scores using TF-IDF + Cosine Similarity (NLP)'],
  [Flag, 'Flags matches above 15% threshold and auto-generates PDF evidence reports'],
  [BarChart3, 'Dashboard shows analytics: risk distribution, score bands, integrity score'],
]

const techStack = [
  { label: 'Database', value: 'MySQL 8.0', sub: 'InnoDB Engine' },
  { label: 'Backend', value: 'Python 3.11 + FastAPI', sub: 'Uvicorn ASGI Server' },
  { label: 'Frontend', value: 'React 19 + Vite 8', sub: 'Modern SPA' },
  { label: 'NLP / ML', value: 'scikit-learn', sub: 'TF-IDF Vectorizer + NLTK' },
  { label: 'File Parsing', value: 'PyPDF2 + python-docx', sub: 'PDF, DOCX, TXT' },
  { label: 'Report Gen', value: 'ReportLab', sub: 'Dynamic PDF generation' },
  { label: 'API Docs', value: 'Swagger UI + ReDoc', sub: 'Auto-generated OpenAPI' },
  { label: 'Architecture', value: 'REST API', sub: 'Modular MVC pattern' },
]

const techIcons = [Database, Server, Braces, Sparkles, FileCode2, FileCode2, Workflow, Network]

export default function OverviewSlide() {
  return (
    <>
      <Reveal className="section-header">
        <div className="section-badge">02 - Overview</div>
        <h2 className="section-title">Project Overview & Tech Stack</h2>
        <p className="section-subtitle">A comprehensive platform for detecting textual plagiarism in academic submissions</p>
      </Reveal>
      <div className="two-col">
        <Reveal className="glass-card">
          <h3 className="small-heading flex items-center gap-3">
            <Zap className="h-5 w-5 text-indigo-200" aria-hidden="true" />
            About the Project
          </h3>
          <ul className="feature-list">
            {features.map(([Icon, text], i) => (
              <li key={i}>
                <span className="feature-icon">
                  <Icon className="h-4 w-4" aria-hidden="true" />
                </span>
                <span>{text}</span>
              </li>
            ))}
          </ul>
        </Reveal>
        <div>
          <h3 className="small-heading flex items-center gap-3">
            <Zap className="h-5 w-5 text-indigo-200" aria-hidden="true" />
            Tech Stack
          </h3>
          <Stagger className="tech-grid">
            {techStack.map((t, i) => {
              const Icon = techIcons[i] || Layers3
              return (
                <MotionCard className="tech-card" key={i}>
                  <Icon className="mb-5 h-7 w-7 text-indigo-200" aria-hidden="true" />
                  <div className="tech-card-label">{t.label}</div>
                  <div className="tech-card-value">{t.value}</div>
                  <div className="tech-card-sub">{t.sub}</div>
                </MotionCard>
              )
            })}
          </Stagger>
        </div>
      </div>
    </>
  )
}
