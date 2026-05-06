import React from 'react'
import { BookOpen, FileText, KeyRound, Link2, Lock, ShieldCheck, Table2, UserRound, Zap } from 'lucide-react'
import { MotionCard, Reveal, Stagger } from '../components/Motion.jsx'

const tables = [
  { name: 'User', Icon: UserRound, columns: [
    { name: 'user_id', badge: 'PK', type: 'pk' }, { name: 'first_name' }, { name: 'last_name' },
    { name: 'email', badge: 'UNIQUE', type: 'unique' }, { name: 'password_hash' },
    { name: 'role', badge: 'ENUM', type: 'enum' }, { name: 'created_at' },
  ]},
  { name: 'Course', Icon: BookOpen, columns: [
    { name: 'course_id', badge: 'PK', type: 'pk' }, { name: 'course_code', badge: 'UNIQUE', type: 'unique' },
    { name: 'course_name' }, { name: 'instructor_id', badge: 'FK->User', type: 'fk' },
  ]},
  { name: 'Assignment', Icon: FileText, columns: [
    { name: 'assignment_id', badge: 'PK', type: 'pk' }, { name: 'course_id', badge: 'FK->Course', type: 'fk' },
    { name: 'title' }, { name: 'description' }, { name: 'due_date' },
  ]},
  { name: 'Submission', Icon: FileText, columns: [
    { name: 'submission_id', badge: 'PK', type: 'pk' }, { name: 'assignment_id', badge: 'FK->Assign', type: 'fk' },
    { name: 'student_id', badge: 'FK->User', type: 'fk' }, { name: 'attempt_number' },
  ]},
  { name: 'Document', Icon: FileText, columns: [
    { name: 'document_id', badge: 'PK', type: 'pk' }, { name: 'submission_id', badge: 'FK->Sub', type: 'fk' },
    { name: 'file_name' }, { name: 'file_path' }, { name: 'file_hash' }, { name: 'extracted_text' },
  ]},
  { name: 'Similarity', Icon: Link2, columns: [
    { name: 'similarity_id', badge: 'PK', type: 'pk' }, { name: 'doc1_id', badge: 'FK->Doc', type: 'fk' },
    { name: 'doc2_id', badge: 'FK->Doc', type: 'fk' }, { name: 'algorithm_id', badge: 'FK->Algo', type: 'fk' },
    { name: 'score' }, { name: 'compared_at' },
  ]},
  { name: 'Report', Icon: Table2, columns: [
    { name: 'report_id', badge: 'PK', type: 'pk' }, { name: 'similarity_id', badge: 'FK->Sim', type: 'fk' },
    { name: 'generated_by', badge: 'FK->User', type: 'fk' }, { name: 'summary_notes' }, { name: 'report_pdf_path' },
  ]},
  { name: 'Algorithm', Icon: Zap, columns: [
    { name: 'algorithm_id', badge: 'PK', type: 'pk' }, { name: 'name', badge: 'UNIQUE', type: 'unique' },
    { name: 'version' }, { name: 'description' },
  ]},
]

const relationships = [
  { from: 'User', to: 'Course', label: '1:M', note: 'instructor' },
  { from: 'User', to: 'Submission', label: '1:M', note: 'student' },
  { from: 'Course', to: 'Assignment', label: '1:M' },
  { from: 'Assignment', to: 'Submission', label: '1:M' },
  { from: 'Submission', to: 'Document', label: '1:M' },
  { from: 'Doc <-> Doc', to: 'Similarity', label: 'M:N', note: 'self-ref' },
  { from: 'Similarity', to: 'Report', label: '1:M' },
  { from: 'Algorithm', to: 'Similarity', label: '1:M' },
]

const constraints = [
  { Icon: ShieldCheck, code: 'CHECK (doc1_id < doc2_id)', desc: 'prevents reversed duplicates' },
  { Icon: ShieldCheck, code: 'UNIQUE (doc1_id, doc2_id, algo_id)', desc: 'one score per pair per algo' },
  { Icon: ShieldCheck, code: 'ON DELETE CASCADE', desc: 'clean orphan removal on most FKs' },
  { Icon: Lock, code: 'ON DELETE RESTRICT', desc: 'protects audit trail on Report' },
  { Icon: ShieldCheck, code: "ENUM('student','instructor','admin')", desc: 'restricts valid roles' },
  { Icon: Zap, code: '4 Custom Indexes', desc: 'assignment, composite, file_hash, score' },
]

const badgeClass = (t) => `col-badge badge-${t || ''}`

export default function SchemaSlide() {
  return (
    <>
      <Reveal className="section-header">
        <div className="section-badge">03 - Database</div>
        <h2 className="section-title">Database Design & Schema</h2>
        <p className="section-subtitle">8 Tables, Fully Normalized (3NF)</p>
      </Reveal>

      <Stagger className="schema-grid">
        {tables.map((t, i) => (
          <MotionCard className="table-card" key={i}>
            <div className="table-card-header">
              <div className="table-icon">
                <t.Icon className="h-5 w-5" aria-hidden="true" />
              </div>
              <div className="table-name">{t.name}</div>
            </div>
            <div className="table-card-body">
              {t.columns.map((c, j) => (
                <div className="column-row" key={j}>
                  <span className="col-name">{c.name}</span>
                  {c.badge && <span className={badgeClass(c.type)}>{c.badge}</span>}
                </div>
              ))}
            </div>
          </MotionCard>
        ))}
      </Stagger>

      <Reveal>
        <h3 className="small-heading flex items-center gap-3">
          <Link2 className="h-5 w-5 text-indigo-200" aria-hidden="true" />
          Relationships
        </h3>
      </Reveal>
      <Stagger className="rel-grid">
        {relationships.map((r, i) => (
          <MotionCard className="rel-item" key={i}>
            <span className="text-[0.8rem] font-bold text-slate-50">{r.from}</span>
            <span className="rel-arrow">-&gt;</span>
            <span className="text-[0.8rem] font-bold text-slate-50">{r.to}</span>
            <span className="rel-type">{r.label}</span>
            {r.note && <span className="text-[0.65rem] text-slate-500">{r.note}</span>}
          </MotionCard>
        ))}
      </Stagger>

      <Reveal>
        <h3 className="small-heading flex items-center gap-3">
          <KeyRound className="h-5 w-5 text-indigo-200" aria-hidden="true" />
          Key Constraints & Integrity
        </h3>
      </Reveal>
      <Stagger className="constraints-grid">
        {constraints.map((c, i) => (
          <MotionCard className="constraint-item" key={i}>
            <span className="constraint-icon">
              <c.Icon className="h-4 w-4" aria-hidden="true" />
            </span>
            <div>
              <span className="constraint-code">{c.code}</span>
              <span className="ml-1.5">- {c.desc}</span>
            </div>
          </MotionCard>
        ))}
      </Stagger>
    </>
  )
}
