import { AnimatePresence, motion as Motion } from 'framer-motion';
import { X } from 'lucide-react';

export function Modal({ open, title, subtitle, onClose, children }) {
  return (
    <AnimatePresence>
      {open && (
        <Motion.div
          className="modal-backdrop"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          onClick={onClose}
        >
          <Motion.div
            className="modal-shell"
            initial={{ opacity: 0, y: 20, scale: 0.96 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 16, scale: 0.98 }}
            transition={{ duration: 0.2 }}
            onClick={(event) => event.stopPropagation()}
          >
            <div className="modal-header">
              <div>
                <h3>{title}</h3>
                <p>{subtitle}</p>
              </div>
              <button type="button" className="icon-button" onClick={onClose} aria-label="Close modal">
                <X size={18} />
              </button>
            </div>
            {children}
          </Motion.div>
        </Motion.div>
      )}
    </AnimatePresence>
  );
}
