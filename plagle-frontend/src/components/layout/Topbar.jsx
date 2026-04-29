import { Bell, MoonStar, PanelLeft, Search, SunMedium } from 'lucide-react';

export function Topbar({
  theme,
  onToggleTheme,
  onToggleSidebar,
  sidebarCollapsed,
  activeFile,
  totalFindings,
}) {
  return (
    <header className="topbar">
      <div className="topbar-left">
        <button type="button" className="icon-button topbar-toggle" onClick={onToggleSidebar} aria-label="Toggle sidebar">
          <PanelLeft size={18} />
        </button>
        <div>
          <span className="eyebrow">Premium Review Workspace</span>
          <h1>Plagiarism intelligence dashboard</h1>
        </div>
      </div>

      <div className="topbar-actions">
        <div className="topbar-chip topbar-chip-search">
          <Search size={16} />
          <span>{activeFile || 'No file selected'}</span>
        </div>
        <div className="topbar-chip">
          <Bell size={16} />
          <span>{totalFindings} active findings</span>
        </div>
        <button type="button" className="icon-button" onClick={onToggleTheme} aria-label="Toggle theme">
          {theme === 'dark' ? <SunMedium size={18} /> : <MoonStar size={18} />}
        </button>
        <a href="#scan" className={`button button-secondary button-sm ${sidebarCollapsed ? 'button-inline' : ''}`}>
          Start scan
        </a>
      </div>
    </header>
  );
}
