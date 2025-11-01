import { NavBar } from '../components/NavBar'
import { Card } from '../components/Card'
import { useUser } from '../context/UserContext'

export function Dashboard() {
  const { user } = useUser()

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <NavBar />
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-6">
          Dashboard
        </h1>
        {user && (
          <div className="mb-6">
            <p className="text-gray-600 dark:text-gray-400">
              Welcome, {user.email || user.name}!
            </p>
          </div>
        )}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <Card>
            <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
              Analytics
            </h3>
            <p className="text-gray-600 dark:text-gray-400">
              View your health analytics and insights
            </p>
          </Card>
          <Card>
            <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
              Documents
            </h3>
            <p className="text-gray-600 dark:text-gray-400">
              Manage your health documents
            </p>
          </Card>
          <Card>
            <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
              Reports
            </h3>
            <p className="text-gray-600 dark:text-gray-400">
              Generate and view reports
            </p>
          </Card>
        </div>
      </main>
    </div>
  )
}

