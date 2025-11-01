import { NavBar } from '../components/NavBar'

export function Home() {
  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <NavBar />
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
            Welcome to Health AI Platform
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-400">
            Intelligent healthcare data processing and analysis
          </p>
        </div>
      </main>
    </div>
  )
}

