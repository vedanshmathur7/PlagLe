import React from 'react'
import { BrainCircuit, DatabaseZap, FastForward, KeyRound, LockKeyhole, Route, TriangleAlert, UsersRound } from 'lucide-react'
import { MotionCard, Reveal, Stagger } from '../components/Motion.jsx'

const challenges = [
  'Designing the self-referencing M:N relationship (Document <-> Document via Similarity table) - required careful dual-JOIN paths to avoid Cartesian products',
  'Preventing duplicate/reversed comparisons - solved with CHECK + UNIQUE constraints + Python-side canonical ordering',
  'Building a 7-table JOIN with correct aliasing (u1 vs u2, d1 vs d2) without producing wrong results',
  'Handling file I/O + database transactions atomically - used context managers with rollback on failure',
]

const futureScope = [
  { Icon: LockKeyhole, text: 'JWT-based authentication and role-based access control' },
  { Icon: BrainCircuit, text: 'Additional algorithms (Jaccard Similarity, n-gram fingerprinting)' },
  { Icon: FastForward, text: 'Batch matrix optimization for large classes' },
  { Icon: UsersRound, text: 'Student enrollment via Course_Enrollment junction table' },
  { Icon: DatabaseZap, text: 'Caching extracted text to avoid re-parsing files' },
]

export default function HighlightsSlide() {
  return (
    <>
      <Reveal className="section-header">
        <div className="section-badge">05 - Highlights</div>
        <h2 className="section-title">Highlights, Challenges & Future Scope</h2>
        <p className="section-subtitle">Key achievements, obstacles overcome, and the road ahead</p>
      </Reveal>

      <div className="two-col mb-10">
        <Reveal>
          <h3 className="small-heading flex items-center gap-3">
            <Route className="h-5 w-5 text-indigo-200" aria-hidden="true" />
            Complex SQL - 7-Table JOIN
          </h3>
          <div className="code-block">
            <div className="code-block-header">
              <span className="code-dot code-dot-red"></span>
              <span className="code-dot code-dot-yellow"></span>
              <span className="code-dot code-dot-green"></span>
              <span className="ml-2 font-mono text-[0.68rem] text-slate-500">
                report_query.sql
              </span>
            </div>
            <pre>{`-- 7-Table JOIN for PDF Report Generation

Similarity
  -> Algorithm        (algorithm used)
  -> Document d1      (first document)
    -> Submission s1  (first submission)
      -> User u1      (first student)
  -> Document d2      (second document)
    -> Submission s2  (second submission)
      -> User u2      (second student)
  -> Submission s1
    -> Assignment     (assignment title)
      -> Course       (course code)

-- Also used: UPSERT pattern
-- INSERT ... ON DUPLICATE KEY UPDATE
-- Re-run updates existing score`}</pre>
          </div>
        </Reveal>

        <Reveal>
          <h3 className="small-heading flex items-center gap-3">
            <TriangleAlert className="h-5 w-5 text-indigo-200" aria-hidden="true" />
            Challenges Faced
          </h3>
          <ul className="challenge-list">
            {challenges.map((c, i) => (
              <li key={i}>
                <span className="challenge-num">{i + 1}</span>
                <span>{c}</span>
              </li>
            ))}
          </ul>
        </Reveal>
      </div>

      <Reveal>
        <h3 className="small-heading center flex items-center justify-center gap-3">
          <KeyRound className="h-5 w-5 text-indigo-200" aria-hidden="true" />
          Future Scope
        </h3>
      </Reveal>
      <Stagger className="future-grid">
        {futureScope.map((f, i) => (
          <MotionCard className="future-item" key={i}>
            <span className="future-icon">
              <f.Icon className="h-4 w-4" aria-hidden="true" />
            </span>
            <span>{f.text}</span>
          </MotionCard>
        ))}
      </Stagger>

      <Reveal className="thank-you">
        <h2>Thank You!</h2>
        <p>Questions?</p>
      </Reveal>
    </>
  )
}
