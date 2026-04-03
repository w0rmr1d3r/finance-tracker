import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid,
  Tooltip, Legend, ResponsiveContainer,
} from 'recharts'
import { MONTHS, sumMonth } from '../utils/finance'

export default function MonthlyBarChart({ positive, negative }) {
  const chartData = MONTHS.map((month) => {
    const pos = sumMonth(positive, month)
    const neg = sumMonth(negative, month)
    return {
      month: month.slice(0, 3),
      Income: pos ? Number(pos.total.toFixed(2)) : 0,
      Expenses: neg ? Number(Math.abs(neg.total).toFixed(2)) : 0,
    }
  })

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg p-5 shadow-sm border border-gray-200 dark:border-gray-700">
      <h3 className="text-sm font-semibold mb-4 text-gray-700 dark:text-gray-300">Monthly Totals</h3>
      <ResponsiveContainer width="100%" height={260}>
        <BarChart data={chartData} margin={{ top: 5, right: 20, left: 10, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
          <XAxis dataKey="month" tick={{ fontSize: 12 }} />
          <YAxis tick={{ fontSize: 12 }} />
          <Tooltip formatter={(v) => v?.toFixed(2)} />
          <Legend />
          <Bar dataKey="Income" fill="#16a34a" radius={[3, 3, 0, 0]} />
          <Bar dataKey="Expenses" fill="#dc2626" radius={[3, 3, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
