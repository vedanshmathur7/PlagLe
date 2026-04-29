export function LoadingSkeleton({ className = '' }) {
  return <div className={`skeleton ${className}`.trim()} aria-hidden="true" />;
}
