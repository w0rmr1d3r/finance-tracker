import { render, screen, waitFor } from '@testing-library/react'
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { MemoryRouter } from 'react-router-dom'
import { FinanceTable } from './components/FinanceTable'
import { UncategorizedTable } from './components/UncategorizedTable'
import { DifferenceTable } from './components/DifferenceTable'
import App from './App'

// ---------------------------------------------------------------------------
// FinanceTable
// ---------------------------------------------------------------------------

describe('FinanceTable', () => {
  it('shows "No data." when data is null', () => {
    render(<FinanceTable data={null} />)
    expect(screen.getByText('No data.')).toBeInTheDocument()
  })

  it('shows "No data." when data is an empty object', () => {
    render(<FinanceTable data={{}} />)
    expect(screen.getByText('No data.')).toBeInTheDocument()
  })

  it('renders all 12 month column headers', () => {
    const data = {
      January: { Salary: { _amount: '1000', _currency_code: 'EUR' } },
    }
    render(<FinanceTable data={data} />)
    const months = [
      'January', 'February', 'March', 'April', 'May', 'June',
      'July', 'August', 'September', 'October', 'November', 'December',
    ]
    for (const month of months) {
      expect(screen.getByRole('columnheader', { name: month })).toBeInTheDocument()
    }
  })

  it('renders a category row with correctly formatted amount', () => {
    const data = {
      January: { Salary: { _amount: '123.45', _currency_code: 'EUR' } },
    }
    render(<FinanceTable data={data} />)
    expect(screen.getByText('Salary')).toBeInTheDocument()
    expect(screen.getByText('123.45 EUR')).toBeInTheDocument()
  })

  it('renders — for a month with no data for that category', () => {
    const data = {
      January: { Salary: { _amount: '123.45', _currency_code: 'EUR' } },
    }
    render(<FinanceTable data={data} />)
    const dashes = screen.getAllByText('—')
    expect(dashes.length).toBe(11)
  })
})

// ---------------------------------------------------------------------------
// UncategorizedTable
// ---------------------------------------------------------------------------

describe('UncategorizedTable', () => {
  it('shows "No uncategorized entries." when entries is null', () => {
    render(<UncategorizedTable entries={null} />)
    expect(screen.getByText('No uncategorized entries.')).toBeInTheDocument()
  })

  it('shows "No uncategorized entries." when entries is an empty array', () => {
    render(<UncategorizedTable entries={[]} />)
    expect(screen.getByText('No uncategorized entries.')).toBeInTheDocument()
  })

  it('renders a row with date, title, and formatted amount', () => {
    const entries = [
      {
        entry_date: '2024-01-15',
        title: 'Supermarket',
        quantity: { _amount: '78.90', _currency_code: 'EUR' },
      },
    ]
    render(<UncategorizedTable entries={entries} />)
    expect(screen.getByText('2024-01-15')).toBeInTheDocument()
    expect(screen.getByText('Supermarket')).toBeInTheDocument()
    expect(screen.getByText('78.90 EUR')).toBeInTheDocument()
  })
})

// ---------------------------------------------------------------------------
// DifferenceTable
// ---------------------------------------------------------------------------

describe('DifferenceTable', () => {
  it('renders h2 "Difference"', () => {
    render(<DifferenceTable positive={null} negative={null} />)
    expect(screen.getByRole('heading', { level: 2, name: 'Difference' })).toBeInTheDocument()
  })

  it('shows "No data." when both positive and negative are empty', () => {
    render(<DifferenceTable positive={{}} negative={{}} />)
    expect(screen.getByText('No data.')).toBeInTheDocument()
  })

  it('renders the correct net difference for a single month', () => {
    const positive = { January: { Salary: { _amount: '1000', _currency_code: 'EUR' } } }
    const negative = { January: { Rent: { _amount: '400', _currency_code: 'EUR' } } }
    render(<DifferenceTable positive={positive} negative={negative} />)
    expect(screen.getByText('600.00 EUR')).toBeInTheDocument()
  })

  it('shows — for months with no data', () => {
    const positive = { January: { Salary: { _amount: '1000', _currency_code: 'EUR' } } }
    render(<DifferenceTable positive={positive} negative={{}} />)
    const dashes = screen.getAllByText('—')
    expect(dashes.length).toBe(11)
  })
})

// ---------------------------------------------------------------------------
// App integration (mocked fetch)
// ---------------------------------------------------------------------------

describe('App', () => {
  beforeEach(() => {
    vi.spyOn(globalThis, 'fetch')
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('shows "Loading..." while fetch is pending', () => {
    globalThis.fetch.mockReturnValue(new Promise(() => {}))
    render(
      <MemoryRouter initialEntries={['/dashboard']}>
        <App />
      </MemoryRouter>
    )
    expect(screen.getByText('Loading...')).toBeInTheDocument()
  })

  it('shows an error message when fetch rejects', async () => {
    globalThis.fetch.mockRejectedValue(new Error('Network error'))
    render(
      <MemoryRouter initialEntries={['/dashboard']}>
        <App />
      </MemoryRouter>
    )
    await waitFor(() =>
      expect(screen.getByText(/Error loading data: Network error/)).toBeInTheDocument()
    )
  })

  it('renders dashboard cards when data loads', async () => {
    const mockData = {
      positive: { January: { Salary: { _amount: '1000', _currency_code: 'EUR' } } },
      negative: {},
      uncategorized: [],
    }
    globalThis.fetch.mockResolvedValue({
      ok: true,
      json: () => Promise.resolve(mockData),
    })
    render(
      <MemoryRouter initialEntries={['/dashboard']}>
        <App />
      </MemoryRouter>
    )
    await waitFor(() =>
      expect(screen.getByText('Total Income')).toBeInTheDocument()
    )
    expect(screen.getByText('Total Expenses')).toBeInTheDocument()
    expect(screen.getByText('Net Difference')).toBeInTheDocument()
    expect(screen.getByText('Savings Rate')).toBeInTheDocument()
  })
})
