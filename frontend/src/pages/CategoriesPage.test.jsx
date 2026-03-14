import { render, screen, waitFor, fireEvent } from '@testing-library/react'
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { MemoryRouter } from 'react-router-dom'
import { DataProvider } from '../context/DataContext'
import CategoriesPage from './CategoriesPage'

const mockData = {
  positive: {},
  negative: {},
  uncategorized: [
    {
      entry_date: '2024-03-01',
      title: 'Mystery Shop',
      other_data: 'some desc',
      quantity: { _amount: '50', _currency_code: 'EUR' },
    },
  ],
}

const mockCategories = {
  categories: { GROCERIES: ['Tesco'], SALARY: ['Employer'] },
  positive_categories: ['SALARY'],
}

function renderPage() {
  return render(
    <MemoryRouter>
      <DataProvider>
        <CategoriesPage />
      </DataProvider>
    </MemoryRouter>
  )
}

describe('CategoriesPage', () => {
  beforeEach(() => {
    vi.spyOn(globalThis, 'fetch').mockImplementation((url) => {
      if (url === '/data') {
        return Promise.resolve({ ok: true, json: () => Promise.resolve(mockData) })
      }
      if (url === '/categories') {
        return Promise.resolve({ ok: true, json: () => Promise.resolve(mockCategories) })
      }
      if (url === '/categories/create') {
        const updatedCategories = {
          categories: { GROCERIES: ['Tesco'], SALARY: ['Employer'], Transport: [] },
          positive_categories: ['SALARY'],
        }
        return Promise.resolve({ ok: true, json: () => Promise.resolve(updatedCategories) })
      }
      return Promise.resolve({ ok: true, json: () => Promise.resolve(mockData) })
    })
  })
  afterEach(() => { vi.restoreAllMocks() })

  it('renders defined category names', async () => {
    renderPage()
    await waitFor(() => expect(screen.getAllByText('GROCERIES').length).toBeGreaterThanOrEqual(1))
    expect(screen.getAllByText('SALARY').length).toBeGreaterThanOrEqual(1)
  })

  it('shows income/expense type badges', async () => {
    renderPage()
    await waitFor(() => expect(screen.getAllByText('SALARY').length).toBeGreaterThanOrEqual(1))
    expect(screen.getAllByText('Income').length).toBeGreaterThanOrEqual(1)
    expect(screen.getAllByText('Expense').length).toBeGreaterThanOrEqual(1)
  })

  it('renders uncategorized entry in assign section', async () => {
    renderPage()
    await waitFor(() => expect(screen.getByText('Mystery Shop')).toBeInTheDocument())
  })

  it('calls POST /categories/assign on Assign click and triggers refetch', async () => {
    renderPage()
    await waitFor(() => expect(screen.getByText('Mystery Shop')).toBeInTheDocument())

    const select = screen.getByRole('combobox')
    fireEvent.change(select, { target: { value: 'GROCERIES' } })
    fireEvent.click(screen.getByText('Assign'))

    await waitFor(() =>
      expect(globalThis.fetch).toHaveBeenCalledWith(
        '/categories/assign',
        expect.objectContaining({ method: 'POST' })
      )
    )
  })

  it('renders the create category form', async () => {
    renderPage()
    await waitFor(() => expect(screen.getByPlaceholderText('NEW CATEGORY NAME')).toBeInTheDocument())
    expect(screen.getByText('Create Category')).toBeInTheDocument()
  })

  it('calls POST /categories/create and updates the category list', async () => {
    renderPage()
    await waitFor(() => expect(screen.getByPlaceholderText('NEW CATEGORY NAME')).toBeInTheDocument())

    fireEvent.change(screen.getByPlaceholderText('NEW CATEGORY NAME'), { target: { value: 'Transport' } })
    fireEvent.click(screen.getByText('Create Category'))

    await waitFor(() =>
      expect(globalThis.fetch).toHaveBeenCalledWith(
        '/categories/create',
        expect.objectContaining({ method: 'POST' })
      )
    )
  })

  it('row selection for an entry is preserved after refetch removes an earlier entry', async () => {
    const entryA = { entry_date: '2024-03-01', title: 'Entry A', quantity: { _amount: '10', _currency_code: 'EUR' } }
    const entryB = { entry_date: '2024-03-02', title: 'Entry B', quantity: { _amount: '20', _currency_code: 'EUR' } }

    let dataCallCount = 0
    globalThis.fetch.mockImplementation((url) => {
      if (url === '/data') {
        dataCallCount++
        const uncategorized = dataCallCount === 1 ? [entryA, entryB] : [entryB]
        return Promise.resolve({ ok: true, json: () => Promise.resolve({ positive: {}, negative: {}, uncategorized }) })
      }
      if (url === '/categories') {
        return Promise.resolve({ ok: true, json: () => Promise.resolve(mockCategories) })
      }
      return Promise.resolve({ ok: true, json: () => Promise.resolve({}) })
    })

    renderPage()
    await waitFor(() => expect(screen.getByText('Entry A')).toBeInTheDocument())
    await waitFor(() => expect(screen.getByText('Entry B')).toBeInTheDocument())

    // Select GROCERIES for Entry B (second row — index 1 in the unfiltered list)
    const rowSelects = screen.getAllByRole('combobox')
    // [0] = Entry A's select, [1] = Entry B's select
    fireEvent.change(rowSelects[1], { target: { value: 'GROCERIES' } })

    // Assign Entry A, which triggers a refetch removing it from the list
    fireEvent.change(rowSelects[0], { target: { value: 'SALARY' } })
    fireEvent.click(screen.getAllByText('Assign')[0])

    // After refetch only Entry B remains (was at index 1, now at index 0)
    await waitFor(() => expect(screen.queryByText('Entry A')).not.toBeInTheDocument())

    // Entry B's select should still show the value we set, not reset to empty
    const remainingSelect = screen.getByRole('combobox')
    expect(remainingSelect.value).toBe('GROCERIES')
  })

  it('assign after refetch shrinks the list sends the correct entry title', async () => {
    const entryA = { entry_date: '2024-03-01', title: 'Entry A', quantity: { _amount: '10', _currency_code: 'EUR' } }
    const entryB = { entry_date: '2024-03-02', title: 'Entry B', quantity: { _amount: '20', _currency_code: 'EUR' } }

    let dataCallCount = 0
    globalThis.fetch.mockImplementation((url) => {
      if (url === '/data') {
        dataCallCount++
        const uncategorized = dataCallCount === 1 ? [entryA, entryB] : [entryB]
        return Promise.resolve({ ok: true, json: () => Promise.resolve({ positive: {}, negative: {}, uncategorized }) })
      }
      if (url === '/categories') {
        return Promise.resolve({ ok: true, json: () => Promise.resolve(mockCategories) })
      }
      return Promise.resolve({ ok: true, json: () => Promise.resolve({}) })
    })

    renderPage()
    await waitFor(() => expect(screen.getByText('Entry A')).toBeInTheDocument())

    // Assign Entry A, triggering a refetch that removes it (Entry B moves to index 0)
    fireEvent.change(screen.getAllByRole('combobox')[0], { target: { value: 'SALARY' } })
    fireEvent.click(screen.getAllByText('Assign')[0])
    await waitFor(() => expect(screen.queryByText('Entry A')).not.toBeInTheDocument())

    // Select a category for Entry B (now the only row, at index 0)
    fireEvent.change(screen.getByRole('combobox'), { target: { value: 'GROCERIES' } })
    fireEvent.click(screen.getByText('Assign'))

    await waitFor(() =>
      expect(globalThis.fetch).toHaveBeenCalledWith(
        '/categories/assign',
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify({ title: 'Entry B', category: 'GROCERIES' }),
        })
      )
    )
  })

  it('calls DELETE /categories/:name on confirm and removes from list', async () => {
    renderPage()
    await waitFor(() => expect(screen.getAllByText('GROCERIES').length).toBeGreaterThanOrEqual(1))

    // Click trash icon on GROCERIES card
    fireEvent.click(screen.getByRole('button', { name: 'Delete GROCERIES' }))

    // Confirm prompt appears
    await waitFor(() => expect(screen.getByText('Delete?')).toBeInTheDocument())

    // Mock the DELETE response
    globalThis.fetch.mockImplementationOnce(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve({
          categories: { SALARY: ['Employer'] },
          positive_categories: ['SALARY'],
        }),
      })
    )

    fireEvent.click(screen.getByText('✓'))

    await waitFor(() =>
      expect(globalThis.fetch).toHaveBeenCalledWith(
        '/categories/GROCERIES',
        expect.objectContaining({ method: 'DELETE' })
      )
    )
    // GROCERIES card should be gone
    await waitFor(() => expect(screen.queryByText('GROCERIES')).not.toBeInTheDocument())
  })
})
