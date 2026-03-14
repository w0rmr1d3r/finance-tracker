import { Navigate, Route, Routes } from 'react-router-dom'
import { DataProvider } from './context/DataContext'
import Layout from './components/Layout'
import DashboardPage from './pages/DashboardPage'
import IncomePage from './pages/IncomePage'
import ExpensesPage from './pages/ExpensesPage'
import ReportsPage from './pages/ReportsPage'
import CategoriesPage from './pages/CategoriesPage'
import EntriesPage from './pages/EntriesPage'
import SettingsPage from './pages/SettingsPage'

export default function App() {
  return (
    <DataProvider>
      <Layout>
        <Routes>
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/income" element={<IncomePage />} />
          <Route path="/expenses" element={<ExpensesPage />} />
          <Route path="/reports" element={<ReportsPage />} />
          <Route path="/categories" element={<CategoriesPage />} />
          <Route path="/entries" element={<EntriesPage />} />
          <Route path="/settings" element={<SettingsPage />} />
        </Routes>
      </Layout>
    </DataProvider>
  )
}
