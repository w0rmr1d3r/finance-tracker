import { useState } from 'react'

const PAGE_SIZE = 20

export function UncategorizedTable({ entries }) {
  const [search, setSearch] = useState('')
  const [sortCol, setSortCol] = useState(null)
  const [sortDir, setSortDir] = useState('asc')
  const [page, setPage] = useState(0)

  if (!entries || entries.length === 0) {
    return (
      <section className="mb-8">
        <h2 className="text-lg font-semibold mb-2">Uncategorized</h2>
        <p className="text-gray-500 dark:text-gray-400">No uncategorized entries.</p>
      </section>
    )
  }

  function handleSort(col) {
    if (sortCol === col) {
      setSortDir((d) => (d === 'asc' ? 'desc' : 'asc'))
    } else {
      setSortCol(col)
      setSortDir('asc')
    }
    setPage(0)
  }

  const filtered = entries.filter((e) =>
    e.title.toLowerCase().includes(search.toLowerCase())
  )

  function parseDMY(s) {
    const [d, m, y] = s.split('/')
    return new Date(+y, +m - 1, +d).getTime()
  }

  const sorted = [...filtered].sort((a, b) => {
    if (!sortCol) return 0
    let va, vb
    if (sortCol === 'date') {
      va = parseDMY(a.entry_date)
      vb = parseDMY(b.entry_date)
    } else {
      va = Number(a.quantity._amount)
      vb = Number(b.quantity._amount)
    }
    if (va < vb) return sortDir === 'asc' ? -1 : 1
    if (va > vb) return sortDir === 'asc' ? 1 : -1
    return 0
  })

  const totalPages = Math.ceil(sorted.length / PAGE_SIZE)
  const paginated = sorted.slice(page * PAGE_SIZE, (page + 1) * PAGE_SIZE)

  function SortIcon({ col }) {
    if (sortCol !== col) return <span className="ml-1 text-gray-400">↕</span>
    return <span className="ml-1">{sortDir === 'asc' ? '↑' : '↓'}</span>
  }

  return (
    <section className="mb-8">
      <h2 className="text-lg font-semibold mb-3">Uncategorized</h2>
      <div className="mb-3">
        <input
          type="text"
          placeholder="Search by title..."
          value={search}
          onChange={(e) => { setSearch(e.target.value); setPage(0) }}
          className="w-full max-w-sm rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
        />
      </div>
      <div className="overflow-x-auto rounded-lg border border-gray-200 dark:border-gray-700">
        <table className="min-w-full text-sm">
          <thead>
            <tr className="bg-gray-100 dark:bg-gray-800">
              <th
                className="px-4 py-2 text-left font-semibold whitespace-nowrap cursor-pointer select-none"
                onClick={() => handleSort('date')}
              >
                Date <SortIcon col="date" />
              </th>
              <th className="px-4 py-2 text-left font-semibold whitespace-nowrap">Title</th>
              <th
                className="px-4 py-2 text-left font-semibold whitespace-nowrap cursor-pointer select-none"
                onClick={() => handleSort('amount')}
              >
                Amount <SortIcon col="amount" />
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100 dark:divide-gray-700">
            {paginated.map((entry, i) => (
              <tr key={i} className="hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors">
                <td className="px-4 py-2 whitespace-nowrap">{entry.entry_date}</td>
                <td className="px-4 py-2 whitespace-nowrap">{entry.title}</td>
                <td className="px-4 py-2 whitespace-nowrap">
                  {`${Number(entry.quantity._amount).toFixed(2)} ${entry.quantity._currency_code}`}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {totalPages > 1 && (
        <div className="flex items-center justify-between mt-3 text-sm">
          <span className="text-gray-500 dark:text-gray-400">
            Page {page + 1} of {totalPages} ({sorted.length} results)
          </span>
          <div className="flex gap-2">
            <button
              onClick={() => setPage((p) => Math.max(0, p - 1))}
              disabled={page === 0}
              className="px-3 py-1 rounded border border-gray-300 dark:border-gray-600 disabled:opacity-40 hover:bg-gray-100 dark:hover:bg-gray-700"
            >
              Prev
            </button>
            <button
              onClick={() => setPage((p) => Math.min(totalPages - 1, p + 1))}
              disabled={page === totalPages - 1}
              className="px-3 py-1 rounded border border-gray-300 dark:border-gray-600 disabled:opacity-40 hover:bg-gray-100 dark:hover:bg-gray-700"
            >
              Next
            </button>
          </div>
        </div>
      )}
    </section>
  )
}
