import { useData } from '../context/DataContext'
import { DifferenceTable } from '../components/DifferenceTable'
import IncomeExpensesChart from '../charts/IncomeExpensesChart'

export default function ReportsPage() {
  const { data, loading, error } = useData()
  if (loading) return <p className="text-gray-500">Loading...</p>
  if (error) return <p className="text-red-600">Error loading data: {error}</p>
  return (
    <div className="space-y-6">
      <DifferenceTable positive={data?.positive} negative={data?.negative} />
      <IncomeExpensesChart positive={data?.positive} negative={data?.negative} />
    </div>
  )
}
