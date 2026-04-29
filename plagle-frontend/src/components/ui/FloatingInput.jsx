export function FloatingInput({ label, value, onChange, id, type = 'text', min, required = false }) {
  return (
    <label className="floating-field" htmlFor={id}>
      <input
        id={id}
        type={type}
        value={value}
        min={min}
        placeholder=" "
        onChange={(event) => onChange(event.target.value)}
        required={required}
      />
      <span>{label}</span>
    </label>
  );
}
