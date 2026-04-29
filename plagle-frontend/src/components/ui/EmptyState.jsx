export function EmptyState({ badge, title, description, className = '' }) {
  return (
    <div className={`empty-state ${className}`.trim()}>
      <span className="empty-badge">{badge}</span>
      <h3>{title}</h3>
      <p>{description}</p>
    </div>
  );
}
