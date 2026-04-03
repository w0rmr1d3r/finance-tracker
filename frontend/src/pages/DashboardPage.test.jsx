import { render, screen, waitFor, fireEvent } from '@testing-library/react'
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { MemoryRouter } from 'react-router-dom'
import { DataProvider } from '../context/DataContext'
import DashboardPage from './DashboardPage'

const mockData = {
  positive: {
    January: { Salary: { _amount: '2000', _currency_code: 'EUR' } },
    March: { Salary: { _amount: '3000', _currency_code: 'EUR' } },
  },
  negative: {
    January: { Rent: { _amount: '800', _currency_code: 'EUR' } },
  },
  uncategorized: [],
}

function renderDashboard() {
  return render(
    <MemoryRouter>
      <DataProvider>
        <DashboardPage />
      </DataProvider>
    </MemoryRouter>
  )
}

describe('DashboardPage', () => {
  beforeEach(() => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue({
      ok: true,
      json: () => Promise.resolve(mockData),
    })
  })
  afterEach(() => { vi.restoreAllMocks() })

  it('shows loading initially', () => {
    globalThis.fetch.mockReturnValue(new Promise(() => {}))
    renderDashboard()
    expect(screen.getByText('Loading...')).toBeInTheDocument()
  })

  it('renders all 4 summary cards after data loads', async () => {
    renderDashboard()
    await waitFor(() => expect(screen.getByText('Total Income')).toBeInTheDocument())
    expect(screen.getByText('Total Expenses')).toBeInTheDocument()
    expect(screen.getByText('Net Difference')).toBeInTheDocument()
    expect(screen.getByText('Savings Rate')).toBeInTheDocument()
  })

  it('savings rate card is blue when income exceeds expenses', async () => {
    // income=3000, expenses=0 → savings rate 100% → blue
    renderDashboard()
    await waitFor(() => expect(screen.getByText('Savings Rate')).toBeInTheDocument())
    const card = screen.getByText('Savings Rate').closest('div[class]')
    expect(card.className).toMatch(/border-blue-500/)
  })

  it('savings rate card is red when expenses exceed income', async () => {
    globalThis.fetch.mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({
        positive: { March: { Salary: { _amount: '500', _currency_code: 'EUR' } } },
        negative: { March: { Rent: { _amount: '-1500', _currency_code: 'EUR' } } },
        uncategorized: [],
      }),
    })
    renderDashboard()
    await waitFor(() => expect(screen.getByText('Savings Rate')).toBeInTheDocument())
    const card = screen.getByText('Savings Rate').closest('div[class]')
    expect(card.className).toMatch(/border-red-500/)
  })

  it('savings rate card is gray when there is no income', async () => {
    globalThis.fetch.mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({
        positive: {},
        negative: { March: { Rent: { _amount: '-800', _currency_code: 'EUR' } } },
        uncategorized: [],
      }),
    })
    renderDashboard()
    await waitFor(() => expect(screen.getByText('Savings Rate')).toBeInTheDocument())
    const card = screen.getByText('Savings Rate').closest('div[class]')
    expect(card.className).toMatch(/border-gray-400/)
  })

  it('month selector changes card values', async () => {
    renderDashboard()
    await waitFor(() => expect(screen.getByText('Total Income')).toBeInTheDocument())
    // Default to latest month (March — income 3000, expenses 0)
    // 3000.00 EUR appears in Income and Net Difference cards
    expect(screen.getAllByText('3000.00 EUR').length).toBeGreaterThanOrEqual(1)
    // Switch to January
    fireEvent.change(screen.getByRole('combobox'), { target: { value: 'January' } })
    expect(screen.getAllByText('2000.00 EUR').length).toBeGreaterThanOrEqual(1)
  })
})
