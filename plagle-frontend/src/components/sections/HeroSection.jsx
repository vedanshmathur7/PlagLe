import { motion as Motion } from 'framer-motion';
import { Activity, FileBadge2, ShieldCheck, Sparkles } from 'lucide-react';
import { Card } from '../ui/Card';
import { defaultInsights } from '../../utils/dashboard';

export function HeroSection({ file, metrics, loading }) {
  return (
    <section id="overview" className="hero-section">
      <Card className="hero-card-panel">
        <div className="hero-copy-block">
          <span className="eyebrow">Academic Integrity Workspace</span>
          <h2>Review submissions in a dashboard that feels production-ready, focused, and fast.</h2>
          <p>
            PlagLe now centers the workflow around clear hierarchy, analytics, and reviewer
            confidence instead of raw output blocks.
          </p>
        </div>

        <div className="hero-pill-row">
          <div className="hero-pill">
            <FileBadge2 size={16} />
            <span>{file ? file.name : 'Upload a document to begin'}</span>
          </div>
          <div className="hero-pill">
            <Activity size={16} />
            <span>{loading ? 'Analysis in progress' : 'Submission console ready'}</span>
          </div>
          <div className="hero-pill">
            <ShieldCheck size={16} />
            <span>{metrics.integrityScore.toFixed(0)} integrity score</span>
          </div>
        </div>

        <div className="hero-insights-grid">
          {defaultInsights.map((item, index) => (
            <Motion.div
              key={item.label}
              className="metric-glass-card"
              initial={{ opacity: 0, y: 16 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.05 * index }}
            >
              <span>{item.label}</span>
              <strong>{item.value}</strong>
            </Motion.div>
          ))}
          <div className="metric-glass-card metric-glass-card-accent">
            <span>Reviewer focus</span>
            <strong>{metrics.highRiskCount} high-risk comparisons</strong>
            <div className="metric-inline-note">
              <Sparkles size={15} />
              <span>Surface the riskiest overlaps first.</span>
            </div>
          </div>
        </div>
      </Card>
    </section>
  );
}
