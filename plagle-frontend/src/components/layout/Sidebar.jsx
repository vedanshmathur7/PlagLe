import { BarChart3, FileSearch2, LayoutDashboard, MenuSquare, PanelLeftClose, Sparkles } from 'lucide-react';
import { motion as Motion } from 'framer-motion';
import { navigationItems } from '../../utils/dashboard';

const iconMap = {
  overview: LayoutDashboard,
  scan: FileSearch2,
  analytics: BarChart3,
  findings: MenuSquare,
};

export function Sidebar({ collapsed, onToggle, metrics, hasResult }) {
  return (
    <aside className={`sidebar ${collapsed ? 'sidebar-collapsed' : ''}`}>
      <div className="sidebar-brand">
        <div className="brand-mark">
          <Sparkles size={18} />
        </div>
        {!collapsed && (
          <div>
            <strong>PlagLe</strong>
            <p>Integrity command center</p>
          </div>
        )}
        <button type="button" className="icon-button sidebar-toggle" onClick={onToggle} aria-label="Toggle sidebar">
          <PanelLeftClose size={18} />
        </button>
      </div>

      <nav className="sidebar-nav">
        {navigationItems.map((item) => {
          const Icon = iconMap[item.id];

          return (
            <a key={item.id} href={`#${item.id}`} className="sidebar-link">
              <Icon size={18} />
              {!collapsed && <span>{item.label}</span>}
            </a>
          );
        })}
      </nav>

      <Motion.div
        className="sidebar-summary"
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
      >
        {!collapsed && (
          <>
            <span className="sidebar-summary-label">Review status</span>
            <strong>{hasResult ? `${metrics.totalMatches} findings ready` : 'Awaiting submission'}</strong>
            <p>{hasResult ? `${metrics.highRiskCount} high-risk matches need attention.` : 'Upload a file to start the scan pipeline.'}</p>
          </>
        )}
      </Motion.div>
    </aside>
  );
}
