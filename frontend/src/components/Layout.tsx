import { Link, useLocation } from 'react-router-dom'
import { Database, Beaker, Sparkles } from 'lucide-react'

interface LayoutProps {
  children: React.ReactNode
}

export default function Layout({ children }: LayoutProps) {
  const location = useLocation()

  const isActive = (path: string) => {
    return location.pathname === path || location.pathname.startsWith(path + '/')
  }

  return (
    <div className="min-h-screen flex flex-col relative overflow-hidden">
      {/* Animated background particles */}
      <div className="fixed inset-0 pointer-events-none overflow-hidden">
        <div className="absolute top-20 left-10 w-72 h-72 bg-purple-300 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob"></div>
        <div className="absolute top-40 right-10 w-72 h-72 bg-yellow-300 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob animation-delay-2000"></div>
        <div className="absolute -bottom-8 left-20 w-72 h-72 bg-pink-300 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob animation-delay-4000"></div>
      </div>

      {/* Header with glassmorphism */}
      <header className="glass sticky top-0 z-50 border-b border-white/20 backdrop-blur-xl">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <Link to="/" className="flex items-center space-x-3 group">
              <div className="w-12 h-12 gradient-bg rounded-xl flex items-center justify-center shadow-lg group-hover:scale-110 transition-transform duration-300">
                <Beaker className="w-7 h-7 text-white animate-pulse" />
              </div>
              <div>
                <h1 className="text-xl font-bold bg-gradient-to-r from-primary-600 to-purple-600 bg-clip-text text-transparent">
                  AutoLab Drive
                </h1>
                <p className="text-xs text-gray-600 flex items-center space-x-1">
                  <Sparkles className="w-3 h-3" />
                  <span>Self-Evolving Research System</span>
                </p>
              </div>
            </Link>

            <nav className="flex space-x-2">
              <Link
                to="/"
                className={`px-5 py-2.5 rounded-xl flex items-center space-x-2 transition-all duration-300 font-medium ${
                  location.pathname === '/'
                    ? 'bg-gradient-to-r from-primary-500 to-primary-600 text-white shadow-lg scale-105'
                    : 'text-gray-700 hover:bg-white/60 hover:scale-105'
                }`}
              >
                <Sparkles className="w-4 h-4" />
                <span>Home</span>
              </Link>
              <Link
                to="/datasets"
                className={`px-5 py-2.5 rounded-xl flex items-center space-x-2 transition-all duration-300 font-medium ${
                  isActive('/datasets')
                    ? 'bg-gradient-to-r from-blue-500 to-blue-600 text-white shadow-lg scale-105'
                    : 'text-gray-700 hover:bg-white/60 hover:scale-105'
                }`}
              >
                <Database className="w-4 h-4" />
                <span>Datasets</span>
              </Link>
              <Link
                to="/strategies"
                className={`px-5 py-2.5 rounded-xl flex items-center space-x-2 transition-all duration-300 font-medium ${
                  isActive('/strategies')
                    ? 'bg-gradient-to-r from-purple-500 to-pink-600 text-white shadow-lg scale-105'
                    : 'text-gray-700 hover:bg-white/60 hover:scale-105'
                }`}
              >
                <Beaker className="w-4 h-4" />
                <span>Lab Strategies</span>
              </Link>
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 relative z-10 pb-20">
        {children}
      </main>

      {/* Footer with glassmorphism */}
      <footer className="glass border-t border-white/20 fixed bottom-0 left-0 right-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex justify-between items-center text-sm text-gray-600">
            <p className="flex items-center space-x-2">
              <span>© 2024 AutoLab Drive.</span>
              <span className="hidden md:inline">Built with support from Google DeepMind, Freepik, and Forethought.</span>
            </p>
            <div className="flex space-x-6">
              <a href="#" className="hover:text-primary-600 transition-colors duration-200 hover:scale-110 inline-block">
                Documentation
              </a>
              <a href="#" className="hover:text-primary-600 transition-colors duration-200 hover:scale-110 inline-block">
                GitHub
              </a>
            </div>
          </div>
        </div>
      </footer>

      <style>{`
        @keyframes blob {
          0%, 100% { transform: translate(0px, 0px) scale(1); }
          33% { transform: translate(30px, -50px) scale(1.1); }
          66% { transform: translate(-20px, 20px) scale(0.9); }
        }
        .animate-blob {
          animation: blob 7s infinite;
        }
        .animation-delay-2000 {
          animation-delay: 2s;
        }
        .animation-delay-4000 {
          animation-delay: 4s;
        }
      `}</style>
    </div>
  )
}
