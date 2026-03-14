import { render, screen, waitFor, fireEvent } from '@testing-library/react'
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { MemoryRouter } from 'react-router-dom'
import { DataProvider } from '../context/DataContext'
import EntriesPage from './EntriesPage'

const mockData = {
  positive: {},
  negative: {},
  uncategorized: [],
}

const mockCategories = {
  categories: { GROCERIES: ['Tesco'], SALARY: ['Employer'] },
  positive_categories: ['SALARY'],
}

const mockEntries = [
  {
    entry_date: '01/03/2024',
    title: 'Salary Payment',
    quantity: { _amount: 3000.0, _currency_code: 'EUR' },
    category: 'SALARY',
  },
  {
    entry_date: '05/03/2024',
    title: 'Tesco Shop',
    quantity: { _amount: -45.5, _currency_code: 'EUR' },
    category: 'GROCERIES',
  },
]

function renderPage() {
  return render(
    <MemoryRouter>
      <DataProvider>
        <EntriesPage />
      </DataProvider>
    </MemoryRouter>
  )
}

describe('EntriesPage', () => {
  beforeEach(() => {
    vi.spyOn(globalThis, 'fetch').mockImplementation((url) => {
      if (url === '/data') {
        return Promise.resolve({ ok: true, json: () => Promise.resolve(mockData) })
      }
      if (url === '/categories') {
        return Promise.resolve({ ok: true, json: () => Promise.resolve(mockCategories) })
      }
      if (url === '/entries') {
        return Promise.resolve({ ok: true, json: () => Promise.resolve(mockEntries) })
      }
      return Promise.resolve({ ok: true, json: () => Promise.resolve({}) })
    })
  })
  afterEach(() => { vi.restoreAllMocks() })

  it('renders table rows from mock entries data', async () => {
    renderPage()
    await waitFor(() => expect(screen.getByText('Salary Payment')).toBeInTheDocument())
    expect(screen.getByText('Tesco Shop')).toBeInTheDocument()
    expect(screen.getByText('01/03/2024')).toBeInTheDocument()
    expect(screen.getByText('05/03/2024')).toBeInTheDocument()
  })

  it('category filter hides rows not matching selected category', async () => {
    renderPage()
    await waitFor(() => expect(screen.getByText('Salary Payment')).toBeInTheDocument())

    // Filter to SALARY only
    const filterSelect = screen.getAllByRole('combobox')[0]
    fireEvent.change(filterSelect, { target: { value: 'SALARY' } })

    await waitFor(() => expect(screen.getByText('Salary Payment')).toBeInTheDocument())
    expect(screen.queryByText('Tesco Shop')).not.toBeInTheDocument()
  })

  it('assign flow calls POST /categories/assign and shows Saved!', async () => {
    renderPage()
    await waitFor(() => expect(screen.getByText('Salary Payment')).toBeInTheDocument())

    // The first row (Salary Payment) has category SALARY pre-selected
    // Change the row's category selector (second combobox — first is filter)
    const rowSelects = screen.getAllByRole('combobox')
    // rowSelects[0] = filter, rowSelects[1] = first entry row
    fireEvent.change(rowSelects[1], { target: { value: 'GROCERIES' } })

    fireEvent.click(screen.getAllByText('Assign')[0])

    await waitFor(() =>
      expect(globalThis.fetch).toHaveBeenCalledWith(
        '/categories/assign',
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify({ title: 'Salary Payment', category: 'GROCERIES' }),
        })
      )
    )
    await waitFor(() => expect(screen.getByText('Saved!')).toBeInTheDocument())
  })

  it('row selection is preserved when a filter repositions the entry', async () => {
    renderPage()
    await waitFor(() => expect(screen.getByText('Tesco Shop')).toBeInTheDocument())

    // Change the category select for Tesco Shop (index 1 in the unfiltered list → third combobox)
    const allSelects = screen.getAllByRole('combobox')
    // [0] = filter, [1] = Salary Payment row, [2] = Tesco Shop row
    fireEvent.change(allSelects[2], { target: { value: 'SALARY' } })

    // Filter to GROCERIES — Tesco Shop moves to index 0 in displayedEntries
    fireEvent.change(allSelects[0], { target: { value: 'GROCERIES' } })

    await waitFor(() => expect(screen.queryByText('Salary Payment')).not.toBeInTheDocument())

    // Tesco Shop's select should still reflect the changed value, not revert to its original
    const rowSelects = screen.getAllByRole('combobox')
    // [0] = filter, [1] = Tesco Shop row (now the only row)
    expect(rowSelects[1].value).toBe('SALARY')
  })

  it('assign after filtering sends the correct entry title, not the one at the same index before filtering', async () => {
    renderPage()
    await waitFor(() => expect(screen.getByText('Tesco Shop')).toBeInTheDocument())

    // Filter to GROCERIES so only Tesco Shop is visible (was at index 1, now at index 0)
    const filterSelect = screen.getAllByRole('combobox')[0]
    fireEvent.change(filterSelect, { target: { value: 'GROCERIES' } })

    await waitFor(() => expect(screen.queryByText('Salary Payment')).not.toBeInTheDocument())

    fireEvent.click(screen.getByText('Assign'))

    await waitFor(() =>
      expect(globalThis.fetch).toHaveBeenCalledWith(
        '/categories/assign',
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify({ title: 'Tesco Shop', category: 'GROCERIES' }),
        })
      )
    )
  })

  it('error state shows per-row error message on failed assign', async () => {
    renderPage()
    await waitFor(() => expect(screen.getByText('Salary Payment')).toBeInTheDocument())

    // Override fetch for the assign call to fail
    globalThis.fetch.mockImplementationOnce((url) => {
      if (url === '/categories/assign') {
        return Promise.resolve({
          ok: false,
          json: () => Promise.resolve({ detail: 'Server error' }),
        })
      }
      return Promise.resolve({ ok: true, json: () => Promise.resolve({}) })
    })

    const rowSelects = screen.getAllByRole('combobox')
    fireEvent.change(rowSelects[1], { target: { value: 'GROCERIES' } })
    fireEvent.click(screen.getAllByText('Assign')[0])

    await waitFor(() => expect(screen.getByText('Server error')).toBeInTheDocument())
  })
})
