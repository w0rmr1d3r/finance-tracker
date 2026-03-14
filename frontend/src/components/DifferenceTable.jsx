import { MONTHS, sumMonth } from '../utils/finance'

export function DifferenceTable({ positive, negative }) {
  const hasData =
    Object.keys(positive ?? {}).length > 0 ||
    Object.keys(negative ?? {}).length > 0

  if (!hasData) {
    return (
      <section className="mb-8">
        <h2 className="text-lg font-semibold mb-2">Difference</h2>
        <p className="text-gray-500 dark:text-gray-400">No data.</p>
      </section>
    )
  }

  return (
    <section className="mb-8">
      <h2 className="text-lg font-semibold mb-3">Difference</h2>
      <div className="overflow-x-auto rounded-lg border border-gray-200 dark:border-gray-700">
        <table className="min-w-full text-sm">
          <thead>
            <tr className="bg-gray-100 dark:bg-gray-800">
              <th className="sticky left-0 z-10 bg-gray-100 dark:bg-gray-800 px-4 py-2 text-left font-semibold whitespace-nowrap border-r border-gray-200 dark:border-gray-700">
                Net
              </th>
              {MONTHS.map((month) => (
                <th key={month} className="px-4 py-2 text-left font-semibold whitespace-nowrap">
                  {month}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            <tr className="hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors">
              <td className="sticky left-0 z-10 bg-white dark:bg-gray-900 hover:bg-gray-50 dark:hover:bg-gray-800 px-4 py-2 font-medium whitespace-nowrap border-r border-gray-200 dark:border-gray-700">
                Income − Expenses
              </td>
              {MONTHS.map((month) => {
                const pos = sumMonth(positive, month)
                const neg = sumMonth(negative, month)
                if (!pos && !neg) {
                  return (
                    <td key={month} className="px-4 py-2 whitespace-nowrap text-gray-400 dark:text-gray-600">
                      —
                    </td>
                  )
                }
                const diff = (pos?.total ?? 0) - Math.abs(neg?.total ?? 0)
                const currency = pos?.currency ?? neg?.currency
                const colorClass =
                  diff > 0
                    ? 'text-green-700 dark:text-green-400'
                    : diff < 0
                    ? 'text-red-700 dark:text-red-400'
                    : ''
                return (
                  <td key={month} className={`px-4 py-2 whitespace-nowrap ${colorClass}`}>
                    {`${diff.toFixed(2)} ${currency}`}
                  </td>
                )
              })}
            </tr>
          </tbody>
        </table>
      </div>
    </section>
  )
}
