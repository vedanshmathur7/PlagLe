import { motion as Motion } from 'framer-motion';

export function Card({ children, className = '' }) {
  return (
    <Motion.div
      initial={{ opacity: 0, y: 18 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.35, ease: 'easeOut' }}
      className={`surface-card ${className}`.trim()}
    >
      {children}
    </Motion.div>
  );
}
