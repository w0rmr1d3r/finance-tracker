export const MONTHS = [
  'January', 'February', 'March', 'April', 'May', 'June',
  'July', 'August', 'September', 'October', 'November', 'December',
]

/**
 * Sum all category amounts for one month in a data slice.
 * Returns { total, currency } or null if no entries.
 */
export function sumMonth(data, month) {
  const entries = Object.values(data?.[month] ?? {})
  if (entries.length === 0) return null
  return {
    total: entries.reduce((sum, cell) => sum + Number(cell._amount), 0),
    currency: entries[0]._currency_code,
  }
}

/**
 * Format a money value: "1234.56 EUR"
 */
export function formatMoney(amount, currency) {
  return `${Number(amount).toFixed(2)} ${currency}`
}

/**
 * Return the most recent month name that has data in either positive or negative.
 */
export function getLatestMonth(positive, negative) {
  for (let i = MONTHS.length - 1; i >= 0; i--) {
    const m = MONTHS[i]
    const hasPos = positive?.[m] && Object.keys(positive[m]).length > 0
    const hasNeg = negative?.[m] && Object.keys(negative[m]).length > 0
    if (hasPos || hasNeg) return m
  }
  return MONTHS[MONTHS.length - 1]
}

/**
 * Return unique sorted category names from a data slice (all months combined).
 */
export function getCategories(data) {
  return Array.from(
    new Set(MONTHS.flatMap((month) => Object.keys(data?.[month] ?? {})))
  ).sort()
}
