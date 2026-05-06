import React from 'react'

const challenges = [
  'Designing the self-referencing M:N relationship (Document ↔ Document via Similarity table) — required careful dual-JOIN paths to avoid Cartesian products',
  'Preventing duplicate/reversed comparisons — solved with CHECK + UNIQUE constraints + Python-side canonical ordering',
  'Building a 7-table JOIN with correct aliasing (u1 vs u2, d1 vs d2) without producing wrong results',
  'Handling file I/O + database transactions atomically — used context managers with rollback on failure',
]

const futureScope = [
  { icon: '🔐', text: 'JWT-based authentication and role-based access control' },
  { icon: '🧬', text: 'Additional detection algorithms (Jaccard Similarity, n-gram fingerprinting)' },
  { icon: '⚡', text: 'Batch matrix optimization for comparing large classes efficiently' },
  { icon: '👥', text: 'Student enrollment tracking via a Course_Enrollment junction table' },
  { icon: '💾', text: 'Caching extracted text in the Document table to avoid re-parsing files' },
]

export default function HighlightsSection() {
  return (
    <section className="section" id="highlights">
      <div className="grid-pattern"></div>
      <div className="container section-inner">
        <div className="section-header">
          <div className="section-number">05 — Highlights</div>
          <h2 className="section-title">Highlights, Challenges & Future Scope</h2>
          <p className="section-subtitle">Key technical achievements, obstacles overcome, and the road ahead</p>
        </div>

        <div className="two-col" style={{ marginBottom: 56 }}>
          {/* Left — Complex SQL */}
          <div>
            <h3 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: 16, color: 'var(--text-primary)' }}>
              🧩 Complex SQL Query — 7-Table JOIN
            </h3>
            <div className="code-block">
              <div className="code-block-header">
                <span className="code-dot code-dot-red"></span>
                <span className="code-dot code-dot-yellow"></span>
                <span className="code-dot code-dot-green"></span>
                <span style={{ marginLeft: 8, fontSize: '0.75rem', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>
                  report_query.sql
                </span>
              </div>
              <pre>{`-- 7-Table JOIN for PDF Report Generation
-- Fetches: both student names, file names,
-- algorithm, course code, assignment title,
-- and similarity score — in a single query

Similarity
  → Algorithm           (algorithm used)
  → Document d1         (first document)
    → Submission s1     (first submission)
      → User u1         (first student name)
  → Document d2         (second document)
    → Submission s2     (second submission)
      → User u2         (second student name)
  → Submission s1
    → Assignment        (assignment title)
      → Course          (course code)

-- UPSERT Pattern Used:
-- INSERT ... ON DUPLICATE KEY UPDATE
-- Re-running a comparison updates the
-- existing score instead of failing on
-- the UNIQUE constraint.`}</pre>
            </div>
          </div>

          {/* Right — Challenges */}
          <div>
            <h3 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: 16, color: 'var(--text-primary)' }}>
              ⚠️ Challenges Faced
            </h3>
            <ul className="challenge-list">
              {challenges.map((c, i) => (
                <li key={i}>
                  <span className="challenge-num">{i + 1}</span>
                  <span>{c}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Future Scope */}
        <h3 style={{ fontSize: '1.15rem', fontWeight: 700, marginBottom: 20, color: 'var(--text-primary)', textAlign: 'center' }}>
          🚀 Future Scope
        </h3>
        <div className="future-grid">
          {futureScope.map((f, i) => (
            <div className="future-item" key={i}>
              <span className="future-icon">{f.icon}</span>
              <span>{f.text}</span>
            </div>
          ))}
        </div>

        {/* Thank You */}
        <div className="thank-you">
          <h2>Thank You!</h2>
          <p>Questions?</p>
        </div>
      </div>
    </section>
  )
}
