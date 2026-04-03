import { MONTHS } from '../utils/finance'

export default function MonthSelector({ value, onChange }) {
  return (
    <select
      value={value}
      onChange={(e) => onChange(e.target.value)}
      className="rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
    >
      {MONTHS.map((m) => (
        <option key={m} value={m}>{m}</option>
      ))}
    </select>
  )
}
