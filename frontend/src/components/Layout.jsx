import Sidebar from './Sidebar'
import ThemeToggle from './ThemeToggle'
import { useLocation } from 'react-router-dom'

const PAGE_TITLES = {
  '/dashboard': 'Dashboard',
  '/income': 'Income',
  '/expenses': 'Expenses',
  '/entries': 'Entries',
  '/reports': 'Reports',
  '/categories': 'Categories',
  '/settings': 'Settings',
}

export default function Layout({ children }) {
  const { pathname } = useLocation()
  const title = PAGE_TITLES[pathname] ?? 'Finance Tracker'

  return (
    <div className="flex min-h-screen bg-gray-50 dark:bg-gray-900 dark:text-gray-100">
      <Sidebar />
      <div className="flex flex-col flex-1 min-w-0">
        <header className="flex items-center justify-between px-6 py-4 bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 shrink-0">
          <h1 className="text-xl font-semibold">{title}</h1>
          <ThemeToggle />
        </header>
        <main className="flex-1 overflow-y-auto p-6">
          {children}
        </main>
      </div>
    </div>
  )
}
