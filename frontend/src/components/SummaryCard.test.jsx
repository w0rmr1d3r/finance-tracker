import { render, screen } from '@testing-library/react'
import { describe, it, expect } from 'vitest'
import SummaryCard from './SummaryCard'

describe('SummaryCard', () => {
  it('renders title and value', () => {
    render(<SummaryCard title="Total Income" value="1000.00 EUR" />)
    expect(screen.getByText('Total Income')).toBeInTheDocument()
    expect(screen.getByText('1000.00 EUR')).toBeInTheDocument()
  })

  it('applies green accent border class', () => {
    const { container } = render(<SummaryCard title="T" value="V" accent="green" />)
    expect(container.firstChild.className).toContain('border-green-500')
  })

  it('applies red accent border class', () => {
    const { container } = render(<SummaryCard title="T" value="V" accent="red" />)
    expect(container.firstChild.className).toContain('border-red-500')
  })

  it('applies blue accent border class', () => {
    const { container } = render(<SummaryCard title="T" value="V" accent="blue" />)
    expect(container.firstChild.className).toContain('border-blue-500')
  })

  it('defaults to gray accent when no accent prop given', () => {
    const { container } = render(<SummaryCard title="T" value="V" />)
    expect(container.firstChild.className).toContain('border-gray-400')
  })
})
