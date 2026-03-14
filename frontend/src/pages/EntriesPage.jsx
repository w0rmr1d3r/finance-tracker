import { useEffect, useState } from 'react'
import { useData } from '../context/DataContext'

export default function EntriesPage() {
  const { refetch } = useData()

  const [entries, setEntries] = useState([])
  const [entriesLoading, setEntriesLoading] = useState(true)
  const [entriesError, setEntriesError] = useState(null)

  const [categoriesData, setCategoriesData] = useState(null)
  const [catLoading, setCatLoading] = useState(true)
  const [catError, setCatError] = useState(null)

  const [catFilter, setCatFilter] = useState('')
  const [rowSelections, setRowSelections] = useState({})
  const [rowStatus, setRowStatus] = useState({})

  async function fetchEntries() {
    setEntriesLoading(true)
    setEntriesError(null)
    try {
      const res = await fetch('/entries')
      if (!res.ok) throw new Error(`HTTP ${res.status}`)
      const data = await res.json()
      setEntries(data)
    } catch (e) {
      setEntriesError(e.message)
    } finally {
      setEntriesLoading(false)
    }
  }

  useEffect(() => {
    fetchEntries()
  }, [])

  useEffect(() => {
    fetch('/categories')
      .then((r) => { if (!r.ok) throw new Error(`HTTP ${r.status}`); return r.json() })
      .then((d) => { setCategoriesData(d); setCatLoading(false) })
      .catch((e) => { setCatError(e.message); setCatLoading(false) })
  }, [])

  if (entriesLoading || catLoading) return <p className="text-gray-500">Loading...</p>
  if (entriesError) return <p className="text-red-600">Error loading entries: {entriesError}</p>
  if (catError) return <p className="text-red-600">Error loading categories: {catError}</p>

  const { categories = {} } = categoriesData ?? {}
  const categoryNames = Object.keys(categories).sort()

  const displayedEntries = catFilter
    ? entries.filter((e) => e.category === catFilter)
    : entries

  async function handleAssign(entry, rowId) {
    const category = rowSelections[rowId] ?? entry.category
    if (!category) return
    setRowStatus((s) => ({ ...s, [rowId]: 'loading' }))
    try {
      const res = await fetch('/categories/assign', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: entry.title, category }),
      })
      if (!res.ok) {
        const body = await res.json().catch(() => ({}))
        throw new Error(body.detail ?? `HTTP ${res.status}`)
      }
      setRowStatus((s) => ({ ...s, [rowId]: 'success' }))
      await fetchEntries()
      await refetch()
    } catch (e) {
      setRowStatus((s) => ({ ...s, [rowId]: `error:${e.message}` }))
    }
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-3">
        <label className="text-sm font-medium text-gray-700 dark:text-gray-300">Filter by category:</label>
        <select
          value={catFilter}
          onChange={(e) => setCatFilter(e.target.value)}
          className="rounded border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 px-2 py-1 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
        >
          <option value="">All categories</option>
          {categoryNames.map((cat) => (
            <option key={cat} value={cat}>{cat}</option>
          ))}
        </select>
        <span className="text-sm text-gray-500 dark:text-gray-400">
          {displayedEntries.length} entr{displayedEntries.length !== 1 ? 'ies' : 'y'}
        </span>
      </div>

      {displayedEntries.length === 0 ? (
        <p className="text-gray-500 dark:text-gray-400">No entries found.</p>
      ) : (
        <div className="overflow-x-auto rounded-lg border border-gray-200 dark:border-gray-700">
          <table className="min-w-full text-sm">
            <thead>
              <tr className="bg-gray-100 dark:bg-gray-800">
                <th className="px-4 py-2 text-left font-semibold whitespace-nowrap">Date</th>
                <th className="px-4 py-2 text-left font-semibold whitespace-nowrap">Title</th>
                <th className="px-4 py-2 text-left font-semibold whitespace-nowrap">Amount</th>
                <th className="px-4 py-2 text-left font-semibold whitespace-nowrap">Category</th>
                <th className="px-4 py-2 text-left font-semibold whitespace-nowrap">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100 dark:divide-gray-700">
              {displayedEntries.map((entry) => {
                const rowId = `${entry.entry_date}:${entry.title}`
                const status = rowStatus[rowId]
                const isLoading = status === 'loading'
                const isSuccess = status === 'success'
                const isError = status?.startsWith('error:')
                const errMsg = isError ? status.slice(6) : ''
                const selectedCat = rowSelections[rowId] ?? entry.category
                return (
                  <tr key={rowId} className="hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors">
                    <td className="px-4 py-2 whitespace-nowrap">{entry.entry_date}</td>
                    <td className="px-4 py-2 whitespace-nowrap">{entry.title}</td>
                    <td className="px-4 py-2 whitespace-nowrap">
                      {`${Number(entry.quantity._amount).toFixed(2)} ${entry.quantity._currency_code}`}
                    </td>
                    <td className="px-4 py-2 whitespace-nowrap">
                      <select
                        value={selectedCat}
                        onChange={(e) => setRowSelections((s) => ({ ...s, [rowId]: e.target.value }))}
                        disabled={isLoading}
                        className="rounded border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 px-2 py-1 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                      >
                        <option value="">Select…</option>
                        {categoryNames.map((cat) => (
                          <option key={cat} value={cat}>{cat}</option>
                        ))}
                      </select>
                    </td>
                    <td className="px-4 py-2 whitespace-nowrap">
                      <button
                        onClick={() => handleAssign(entry, rowId)}
                        disabled={!selectedCat || isLoading}
                        className="px-3 py-1 rounded bg-indigo-600 text-white text-xs font-semibold disabled:opacity-40 hover:bg-indigo-700 transition-colors"
                      >
                        {isLoading ? 'Saving…' : 'Assign'}
                      </button>
                      {isSuccess && (
                        <span className="ml-2 text-xs text-green-600 dark:text-green-400">Saved!</span>
                      )}
                      {isError && (
                        <span className="ml-2 text-xs text-red-600 dark:text-red-400">{errMsg}</span>
                      )}
                    </td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
