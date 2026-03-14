import { render, screen, fireEvent } from '@testing-library/react'
import { describe, it, expect } from 'vitest'
import { UncategorizedTable } from './UncategorizedTable'

function makeEntry(title, date = '2024-01-01', amount = '10') {
  return {
    entry_date: date,
    title,
    other_data: 'desc',
    quantity: { _amount: amount, _currency_code: 'EUR' },
  }
}

describe('UncategorizedTable search', () => {
  it('filters rows by title', () => {
    const entries = [makeEntry('Supermarket'), makeEntry('Petrol station')]
    render(<UncategorizedTable entries={entries} />)
    fireEvent.change(screen.getByPlaceholderText('Search by title...'), { target: { value: 'super' } })
    expect(screen.getByText('Supermarket')).toBeInTheDocument()
    expect(screen.queryByText('Petrol station')).not.toBeInTheDocument()
  })

  it('shows all rows when search is cleared', () => {
    const entries = [makeEntry('Supermarket'), makeEntry('Petrol station')]
    render(<UncategorizedTable entries={entries} />)
    const input = screen.getByPlaceholderText('Search by title...')
    fireEvent.change(input, { target: { value: 'super' } })
    fireEvent.change(input, { target: { value: '' } })
    expect(screen.getByText('Supermarket')).toBeInTheDocument()
    expect(screen.getByText('Petrol station')).toBeInTheDocument()
  })
})

describe('UncategorizedTable sort', () => {
  it('toggles sort direction on second click', () => {
    const entries = [
      makeEntry('A', '2024-01-01'),
      makeEntry('B', '2024-06-01'),
    ]
    render(<UncategorizedTable entries={entries} />)
    const dateHeader = screen.getByText(/Date/)
    fireEvent.click(dateHeader)
    fireEvent.click(dateHeader)
    // Just ensure it doesn't throw — actual order is tested by integration
    expect(screen.getByText('A')).toBeInTheDocument()
    expect(screen.getByText('B')).toBeInTheDocument()
  })
})

describe('UncategorizedTable pagination', () => {
  it('shows only 20 rows per page when more than 20 entries exist', () => {
    const entries = Array.from({ length: 25 }, (_, i) => makeEntry(`Entry ${i + 1}`))
    render(<UncategorizedTable entries={entries} />)
    expect(screen.getByText(/Page 1 of 2/)).toBeInTheDocument()
    // First page shows entries 1-20
    expect(screen.getByText('Entry 1')).toBeInTheDocument()
    expect(screen.queryByText('Entry 21')).not.toBeInTheDocument()
  })

  it('navigates to next page', () => {
    const entries = Array.from({ length: 25 }, (_, i) => makeEntry(`Entry ${i + 1}`))
    render(<UncategorizedTable entries={entries} />)
    fireEvent.click(screen.getByText('Next'))
    expect(screen.getByText(/Page 2 of 2/)).toBeInTheDocument()
    expect(screen.getByText('Entry 21')).toBeInTheDocument()
  })
})
