import { createContext, useContext, useEffect, useState } from 'react'

const DataContext = createContext(null)

export function DataProvider({ children }) {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [theme, setTheme] = useState(() => localStorage.getItem('theme') ?? 'light')

  async function fetchData() {
    setLoading(true)
    setError(null)
    try {
      const res = await fetch('/data')
      if (!res.ok) throw new Error(`HTTP ${res.status}`)
      const json = await res.json()
      setData(json)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { fetchData() }, [])

  useEffect(() => {
    document.documentElement.classList.toggle('dark', theme === 'dark')
    localStorage.setItem('theme', theme)
  }, [theme])

  function toggleTheme() {
    setTheme((t) => (t === 'light' ? 'dark' : 'light'))
  }

  return (
    <DataContext.Provider value={{ data, loading, error, theme, toggleTheme, refetch: fetchData }}>
      {children}
    </DataContext.Provider>
  )
}

export function useData() {
  return useContext(DataContext)
}
