import { AnimatePresence, motion as Motion } from 'framer-motion';
import { CheckCircle2, CircleAlert, Info, X } from 'lucide-react';

const toneIcons = {
  success: CheckCircle2,
  error: CircleAlert,
  info: Info,
};

export function ToastStack({ toasts, onDismiss }) {
  return (
    <div className="toast-stack" role="status" aria-live="polite">
      <AnimatePresence>
        {toasts.map((toast) => {
          const Icon = toneIcons[toast.tone] ?? Info;

          return (
            <Motion.div
              key={toast.id}
              className={`toast toast-${toast.tone}`}
              initial={{ opacity: 0, y: 18, scale: 0.96 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: 12, scale: 0.96 }}
            >
              <div className="toast-icon">
                <Icon size={18} />
              </div>
              <div className="toast-copy">
                <strong>{toast.title}</strong>
                <p>{toast.description}</p>
              </div>
              <button type="button" className="icon-button" onClick={() => onDismiss(toast.id)} aria-label="Dismiss notification">
                <X size={16} />
              </button>
            </Motion.div>
          );
        })}
      </AnimatePresence>
    </div>
  );
}
