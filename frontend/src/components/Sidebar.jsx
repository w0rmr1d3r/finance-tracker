import { NavLink } from 'react-router-dom'

const NAV_ITEMS = [
  { to: '/dashboard', label: 'Dashboard' },
  { to: '/income', label: 'Income' },
  { to: '/expenses', label: 'Expenses' },
  { to: '/reports', label: 'Reports' },
  { to: '/entries', label: 'Entries' },
  { to: '/categories', label: 'Categories' },
  { to: '/settings', label: 'Settings' },
]

export default function Sidebar() {
  return (
    <aside className="w-64 shrink-0 bg-gray-900 dark:bg-gray-950 text-gray-100 flex flex-col min-h-screen">
      <div className="px-6 py-5 border-b border-gray-700">
        <span className="text-lg font-bold tracking-tight">Finance Tracker</span>
      </div>
      <nav className="flex-1 px-3 py-4 space-y-1">
        {NAV_ITEMS.map(({ to, label }) => (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) =>
              `block px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                isActive
                  ? 'bg-indigo-600 text-white'
                  : 'text-gray-300 hover:bg-gray-700 hover:text-white'
              }`
            }
          >
            {label}
          </NavLink>
        ))}
      </nav>
    </aside>
  )
}
