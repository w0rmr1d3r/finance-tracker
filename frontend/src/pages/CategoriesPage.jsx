import { useEffect, useState } from 'react'
import { useData } from '../context/DataContext'

export default function CategoriesPage() {
  const { data, loading, error, refetch } = useData()

  const [categoriesData, setCategoriesData] = useState(null)
  const [catLoading, setCatLoading] = useState(true)
  const [catError, setCatError] = useState(null)

  // Per-row selected category state
  const [rowSelections, setRowSelections] = useState({})
  // Per-row status: 'idle' | 'loading' | 'success' | 'error'
  const [rowStatus, setRowStatus] = useState({})

  // Create new category form
  const [newCatName, setNewCatName] = useState('')
  const [newCatType, setNewCatType] = useState('expense')
  const [createStatus, setCreateStatus] = useState('idle')

  // Delete category state
  const [confirmDelete, setConfirmDelete] = useState(null)
  const [deletingCat, setDeletingCat] = useState(null)
  const [deleteError, setDeleteError] = useState({})

  useEffect(() => {
    fetch('/categories')
      .then((r) => { if (!r.ok) throw new Error(`HTTP ${r.status}`); return r.json() })
      .then((d) => { setCategoriesData(d); setCatLoading(false) })
      .catch((e) => { setCatError(e.message); setCatLoading(false) })
  }, [data]) // re-fetch categories when data changes (after assign)

  if (loading || catLoading) return <p className="text-gray-500">Loading...</p>
  if (error) return <p className="text-red-600">Error loading data: {error}</p>
  if (catError) return <p className="text-red-600">Error loading categories: {catError}</p>

  const { categories = {}, positive_categories = [] } = categoriesData ?? {}
  const categoryNames = Object.keys(categories).sort()
  const uncategorized = data?.uncategorized ?? []

  async function handleAssign(entry, rowId) {
    const category = rowSelections[rowId]
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
      await refetch()
    } catch (e) {
      setRowStatus((s) => ({ ...s, [rowId]: `error:${e.message}` }))
    }
  }

  async function handleDelete(catName) {
    setDeletingCat(catName)
    setConfirmDelete(null)
    try {
      const res = await fetch(`/categories/${encodeURIComponent(catName)}`, { method: 'DELETE' })
      const json = await res.json().catch(() => ({}))
      if (!res.ok) throw new Error(json.detail ?? `HTTP ${res.status}`)
      setCategoriesData(json)
    } catch (e) {
      setDeleteError((prev) => ({ ...prev, [catName]: e.message }))
    } finally {
      setDeletingCat(null)
    }
  }

  async function handleCreate(e) {
    e.preventDefault()
    const name = newCatName.trim()
    if (!name) return
    setCreateStatus('loading')
    try {
      const res = await fetch('/categories/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, type: newCatType }),
      })
      const json = await res.json().catch(() => ({}))
      if (!res.ok) throw new Error(json.detail ?? `HTTP ${res.status}`)
      setCategoriesData(json)
      setNewCatName('')
      setNewCatType('expense')
      setCreateStatus('success')
    } catch (e) {
      setCreateStatus(e.message)
    }
  }

  return (
    <div className="space-y-8">
      {/* Section A — Defined Categories */}
      <section>
        <h2 className="text-lg font-semibold mb-4">Defined Categories</h2>
        {categoryNames.length === 0 ? (
          <p className="text-gray-500 dark:text-gray-400">No categories defined yet.</p>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {categoryNames.map((cat) => {
              const isIncome = positive_categories.includes(cat)
              const keywordCount = (categories[cat] ?? []).length
              return (
                <div
                  key={cat}
                  className="relative bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-4 shadow-sm"
                >
                  {/* Trash / confirm controls — top-right */}
                  <div className="absolute top-2 right-2">
                    {deletingCat === cat ? (
                      <span className="text-xs text-gray-400">…</span>
                    ) : confirmDelete === cat ? (
                      <span className="flex items-center gap-1 text-xs">
                        <span className="text-gray-500">Delete?</span>
                        <button onClick={() => handleDelete(cat)} className="text-red-600 hover:text-red-800 font-semibold">✓</button>
                        <button onClick={() => setConfirmDelete(null)} className="text-gray-400 hover:text-gray-600">✕</button>
                      </span>
                    ) : (
                      <button
                        onClick={() => { setConfirmDelete(cat); setDeleteError((p) => ({ ...p, [cat]: undefined })) }}
                        className="text-gray-300 hover:text-red-500 transition-colors"
                        aria-label={`Delete ${cat}`}
                      >
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="w-4 h-4">
                          <path fillRule="evenodd" d="M8.75 1A2.75 2.75 0 006 3.75v.443c-.795.077-1.584.176-2.365.298a.75.75 0 10.23 1.482l.149-.022.841 10.518A2.75 2.75 0 007.596 19h4.807a2.75 2.75 0 002.742-2.53l.841-10.52.149.023a.75.75 0 00.23-1.482A41.03 41.03 0 0014 4.193V3.75A2.75 2.75 0 0011.25 1h-2.5zM10 4c.84 0 1.673.025 2.5.075V3.75c0-.69-.56-1.25-1.25-1.25h-2.5c-.69 0-1.25.56-1.25 1.25v.325C8.327 4.025 9.16 4 10 4zM8.58 7.72a.75.75 0 00-1.5.06l.3 7.5a.75.75 0 101.5-.06l-.3-7.5zm4.34.06a.75.75 0 10-1.5-.06l-.3 7.5a.75.75 0 101.5.06l.3-7.5z" clipRule="evenodd" />
                        </svg>
                      </button>
                    )}
                  </div>

                  <p className="font-bold text-sm mb-2 pr-6">{cat}</p>
                  <span
                    className={`inline-block text-xs font-semibold px-2 py-0.5 rounded-full mb-2 ${
                      isIncome
                        ? 'bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-300'
                        : 'bg-red-100 text-red-700 dark:bg-red-900 dark:text-red-300'
                    }`}
                  >
                    {isIncome ? 'Income' : 'Expense'}
                  </span>
                  <p className="text-xs text-gray-500 dark:text-gray-400">{keywordCount} keyword{keywordCount !== 1 ? 's' : ''}</p>
                  {deleteError[cat] && (
                    <p className="text-xs text-red-500 mt-1">{deleteError[cat]}</p>
                  )}
                </div>
              )
            })}
          </div>
        )}
      </section>

      {/* Section B — Create New Category */}
      <section>
        <h2 className="text-lg font-semibold mb-4">Create New Category</h2>
        <form
          onSubmit={handleCreate}
          className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-5 shadow-sm max-w-md space-y-4"
        >
          <div>
            <label className="block text-sm font-medium mb-1 text-gray-700 dark:text-gray-300">Category name</label>
            <input
              type="text"
              placeholder="NEW CATEGORY NAME"
              value={newCatName}
              onChange={(e) => { setNewCatName(e.target.value); setCreateStatus('idle') }}
              className="w-full rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1 text-gray-700 dark:text-gray-300">Type</label>
            <div className="flex gap-4 text-sm">
              <label className="flex items-center gap-1.5 cursor-pointer">
                <input
                  type="radio"
                  name="newCatType"
                  value="income"
                  checked={newCatType === 'income'}
                  onChange={() => setNewCatType('income')}
                />
                Income
              </label>
              <label className="flex items-center gap-1.5 cursor-pointer">
                <input
                  type="radio"
                  name="newCatType"
                  value="expense"
                  checked={newCatType === 'expense'}
                  onChange={() => setNewCatType('expense')}
                />
                Expense
              </label>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <button
              type="submit"
              disabled={!newCatName.trim() || createStatus === 'loading'}
              className="px-4 py-2 rounded bg-indigo-600 text-white text-sm font-semibold disabled:opacity-40 hover:bg-indigo-700 transition-colors"
            >
              {createStatus === 'loading' ? 'Creating…' : 'Create Category'}
            </button>
            {createStatus === 'success' && (
              <span className="text-sm text-green-600 dark:text-green-400">Category created!</span>
            )}
            {createStatus !== 'idle' && createStatus !== 'loading' && createStatus !== 'success' && (
              <span className="text-sm text-red-600 dark:text-red-400">{createStatus}</span>
            )}
          </div>
        </form>
      </section>

      {/* Section C — Assign Categories */}
      <section>
        <h2 className="text-lg font-semibold mb-4">Assign Categories to Uncategorized Entries</h2>
        {uncategorized.length === 0 ? (
          <p className="text-gray-500 dark:text-gray-400">No uncategorized entries.</p>
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
                {uncategorized.map((entry) => {
                  const rowId = `${entry.entry_date}:${entry.title}`
                  const status = rowStatus[rowId]
                  const isLoading = status === 'loading'
                  const isSuccess = status === 'success'
                  const isError = status?.startsWith('error:')
                  const errMsg = isError ? status.slice(6) : ''
                  return (
                    <tr key={rowId} className="hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors">
                      <td className="px-4 py-2 whitespace-nowrap">{entry.entry_date}</td>
                      <td className="px-4 py-2 whitespace-nowrap">{entry.title}</td>
                      <td className="px-4 py-2 whitespace-nowrap">
                        {`${Number(entry.quantity._amount).toFixed(2)} ${entry.quantity._currency_code}`}
                      </td>
                      <td className="px-4 py-2 whitespace-nowrap">
                        <select
                          value={rowSelections[rowId] ?? ''}
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
                          disabled={!rowSelections[rowId] || isLoading}
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
      </section>
    </div>
  )
}
