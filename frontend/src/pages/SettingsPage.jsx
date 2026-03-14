import { useData } from '../context/DataContext'
import ThemeToggle from '../components/ThemeToggle'

export default function SettingsPage() {
  const { theme } = useData()
  return (
    <div className="max-w-lg space-y-6">
      <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-5 shadow-sm">
        <h2 className="text-base font-semibold mb-4">Appearance</h2>
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm font-medium">Dark Mode</p>
            <p className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">
              Currently: <span className="font-semibold">{theme}</span>
            </p>
          </div>
          <ThemeToggle />
        </div>
      </div>

      <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-5 shadow-sm">
        <h2 className="text-base font-semibold mb-2">About</h2>
        <p className="text-sm text-gray-600 dark:text-gray-400">Finance Tracker v2 — personal finance dashboard.</p>
        <p className="text-xs text-gray-400 dark:text-gray-500 mt-2">Backend: FastAPI · Frontend: React + Vite + Tailwind · Charts: Recharts</p>
      </div>
    </div>
  )
}
