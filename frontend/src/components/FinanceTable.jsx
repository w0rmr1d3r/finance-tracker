import { MONTHS } from '../utils/finance'

const AMOUNT_ACCENT = {
  green: 'text-green-700 dark:text-green-400',
  red: 'text-red-700 dark:text-red-400',
}

export function FinanceTable({ title, data, accentColor }) {
  if (!data || Object.keys(data).length === 0) {
    return (
      <section className="mb-8">
        {title && <h2 className="text-lg font-semibold mb-2">{title}</h2>}
        <p className="text-gray-500 dark:text-gray-400">No data.</p>
      </section>
    )
  }

  const categories = Array.from(
    new Set(MONTHS.flatMap((month) => Object.keys(data[month] ?? {})))
  ).sort()

  const amountClass = AMOUNT_ACCENT[accentColor] ?? ''

  return (
    <section className="mb-8">
      {title && <h2 className="text-lg font-semibold mb-3">{title}</h2>}
      <div className="overflow-x-auto rounded-lg border border-gray-200 dark:border-gray-700">
        <table className="min-w-full text-sm">
          <thead>
            <tr className="bg-gray-100 dark:bg-gray-800">
              <th className="sticky left-0 z-10 bg-gray-100 dark:bg-gray-800 px-4 py-2 text-left font-semibold whitespace-nowrap border-r border-gray-200 dark:border-gray-700">
                Category
              </th>
              {MONTHS.map((month) => (
                <th key={month} className="px-4 py-2 text-left font-semibold whitespace-nowrap">
                  {month}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100 dark:divide-gray-700">
            {categories.map((cat) => (
              <tr key={cat} className="hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors">
                <td className="sticky left-0 z-10 bg-white dark:bg-gray-900 hover:bg-gray-50 dark:hover:bg-gray-800 px-4 py-2 font-medium whitespace-nowrap border-r border-gray-200 dark:border-gray-700">
                  {cat}
                </td>
                {MONTHS.map((month) => {
                  const cell = (data[month] ?? {})[cat]
                  const display = cell
                    ? `${Number(cell._amount).toFixed(2)} ${cell._currency_code}`
                    : '—'
                  return (
                    <td
                      key={month}
                      className={`px-4 py-2 whitespace-nowrap ${cell ? amountClass : 'text-gray-400 dark:text-gray-600'}`}
                    >
                      {display}
                    </td>
                  )
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  )
}
