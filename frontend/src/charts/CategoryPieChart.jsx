import {
  PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer,
} from 'recharts'

const COLORS = [
  '#6366f1', '#f59e0b', '#10b981', '#ef4444', '#3b82f6',
  '#ec4899', '#14b8a6', '#f97316', '#8b5cf6', '#84cc16',
  '#06b6d4', '#e11d48',
]

export default function CategoryPieChart({ negative, selectedMonth }) {
  const monthData = negative?.[selectedMonth] ?? {}
  const slices = Object.entries(monthData).map(([cat, cell]) => ({
    name: cat,
    value: Math.abs(Number(cell._amount)),
    currency: cell._currency_code,
  })).filter((s) => s.value > 0)

  if (slices.length === 0) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-lg p-5 shadow-sm border border-gray-200 dark:border-gray-700 flex items-center justify-center h-48">
        <p className="text-gray-400 text-sm">No expense data for {selectedMonth}</p>
      </div>
    )
  }

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg p-5 shadow-sm border border-gray-200 dark:border-gray-700">
      <h3 className="text-sm font-semibold mb-4 text-gray-700 dark:text-gray-300">
        Expenses by Category — {selectedMonth}
      </h3>
      <ResponsiveContainer width="100%" height={260}>
        <PieChart>
          <Pie
            data={slices}
            cx="50%"
            cy="50%"
            outerRadius={90}
            dataKey="value"
          >
            {slices.map((_, index) => (
              <Cell key={index} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip formatter={(v, _name, props) => [`${v.toFixed(2)} ${props.payload.currency}`, props.payload.name]} />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </div>
  )
}
