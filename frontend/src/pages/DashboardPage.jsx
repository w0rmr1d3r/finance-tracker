import { useState } from 'react'
import { useData } from '../context/DataContext'
import { sumMonth, getLatestMonth, formatMoney } from '../utils/finance'
import SummaryCard from '../components/SummaryCard'
import MonthSelector from '../components/MonthSelector'
import IncomeExpensesChart from '../charts/IncomeExpensesChart'
import MonthlyBarChart from '../charts/MonthlyBarChart'
import CategoryPieChart from '../charts/CategoryPieChart'
import { DifferenceTable } from '../components/DifferenceTable'

export default function DashboardPage() {
  const { data, loading, error } = useData()
  const [selectedMonth, setSelectedMonth] = useState(null)

  if (loading) return <p className="text-gray-500">Loading...</p>
  if (error) return <p className="text-red-600">Error loading data: {error}</p>
  if (!data) return null

  const { positive, negative } = data
  const month = selectedMonth ?? getLatestMonth(positive, negative)

  const posSum = sumMonth(positive, month)
  const negSum = sumMonth(negative, month)
  const income = posSum?.total ?? 0
  const expenses = Math.abs(negSum?.total ?? 0)
  const diff = income - expenses
  const currency = posSum?.currency ?? negSum?.currency ?? ''
  const savingsRateNum = income > 0 ? (diff / income) * 100 : null
  const savingsRate = savingsRateNum !== null ? savingsRateNum.toFixed(1) : '—'

  const diffAccent = diff >= 0 ? 'green' : 'red'
  const savingsAccent = savingsRateNum === null ? 'gray' : savingsRateNum >= 0 ? 'blue' : 'red'

  return (
    <div className="space-y-6">
      {/* Month selector */}
      <div className="flex items-center gap-3">
        <span className="text-sm font-medium text-gray-600 dark:text-gray-400">Viewing month:</span>
        <MonthSelector value={month} onChange={setSelectedMonth} />
      </div>

      {/* Summary cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <SummaryCard title="Total Income" value={formatMoney(income, currency)} accent="green" />
        <SummaryCard title="Total Expenses" value={formatMoney(expenses, currency)} accent="red" />
        <SummaryCard title="Net Difference" value={formatMoney(diff, currency)} accent={diffAccent} />
        <SummaryCard
          title="Savings Rate"
          value={savingsRate === '—' ? '—' : `${savingsRate}%`}
          accent={savingsAccent}
        />
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <IncomeExpensesChart positive={positive} negative={negative} />
        <MonthlyBarChart positive={positive} negative={negative} />
      </div>
      <CategoryPieChart negative={negative} selectedMonth={month} />
      <DifferenceTable positive={positive} negative={negative} />
    </div>
  )
}
