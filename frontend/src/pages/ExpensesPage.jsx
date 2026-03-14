import { useData } from '../context/DataContext'
import { FinanceTable } from '../components/FinanceTable'

export default function ExpensesPage() {
  const { data, loading, error } = useData()
  if (loading) return <p className="text-gray-500">Loading...</p>
  if (error) return <p className="text-red-600">Error loading data: {error}</p>
  return <FinanceTable data={data?.negative} accentColor="red" />
}
