const ACCENT_CLASSES = {
  green: 'border-green-500 text-green-700 dark:text-green-400',
  red: 'border-red-500 text-red-700 dark:text-red-400',
  blue: 'border-blue-500 text-blue-700 dark:text-blue-400',
  gray: 'border-gray-400 text-gray-700 dark:text-gray-300',
}

export default function SummaryCard({ title, value, accent = 'gray' }) {
  const accentClass = ACCENT_CLASSES[accent] ?? ACCENT_CLASSES.gray
  return (
    <div className={`bg-white dark:bg-gray-800 rounded-lg border-l-4 p-5 shadow-sm ${accentClass}`}>
      <p className="text-xs font-semibold uppercase tracking-wider text-gray-500 dark:text-gray-400 mb-1">{title}</p>
      <p className={`text-2xl font-bold ${accentClass.split(' ').slice(1).join(' ')}`}>{value}</p>
    </div>
  )
}
