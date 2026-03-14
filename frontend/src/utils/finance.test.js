import { describe, it, expect } from 'vitest'
import { sumMonth, getLatestMonth, formatMoney, MONTHS } from './finance'

describe('MONTHS', () => {
  it('has 12 entries', () => {
    expect(MONTHS).toHaveLength(12)
  })
  it('starts with January and ends with December', () => {
    expect(MONTHS[0]).toBe('January')
    expect(MONTHS[11]).toBe('December')
  })
})

describe('sumMonth', () => {
  it('returns null for empty data', () => {
    expect(sumMonth({}, 'January')).toBeNull()
  })
  it('returns null when month has no entries', () => {
    expect(sumMonth({ February: { A: { _amount: '10', _currency_code: 'EUR' } } }, 'January')).toBeNull()
  })
  it('sums amounts correctly', () => {
    const data = {
      January: {
        A: { _amount: '100', _currency_code: 'EUR' },
        B: { _amount: '50.5', _currency_code: 'EUR' },
      },
    }
    const result = sumMonth(data, 'January')
    expect(result.total).toBeCloseTo(150.5)
    expect(result.currency).toBe('EUR')
  })
  it('handles null data gracefully', () => {
    expect(sumMonth(null, 'January')).toBeNull()
  })
})

describe('formatMoney', () => {
  it('formats integer amount', () => {
    expect(formatMoney(1000, 'EUR')).toBe('1000.00 EUR')
  })
  it('formats decimal amount', () => {
    expect(formatMoney(1234.5, 'USD')).toBe('1234.50 USD')
  })
  it('formats zero', () => {
    expect(formatMoney(0, 'EUR')).toBe('0.00 EUR')
  })
})

describe('getLatestMonth', () => {
  it('returns the last month with data', () => {
    const positive = {
      March: { Salary: { _amount: '1000', _currency_code: 'EUR' } },
    }
    expect(getLatestMonth(positive, {})).toBe('March')
  })
  it('prefers a later month over an earlier one', () => {
    const positive = {
      January: { A: { _amount: '1', _currency_code: 'EUR' } },
      November: { B: { _amount: '2', _currency_code: 'EUR' } },
    }
    expect(getLatestMonth(positive, {})).toBe('November')
  })
  it('falls back to December if no data', () => {
    expect(getLatestMonth({}, {})).toBe('December')
  })
  it('considers negative data too', () => {
    const negative = {
      June: { Rent: { _amount: '400', _currency_code: 'EUR' } },
    }
    expect(getLatestMonth({}, negative)).toBe('June')
  })
})
