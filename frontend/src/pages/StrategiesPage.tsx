import { useState, useEffect } from 'react'
import { Shield, Zap, TrendingUp, GitBranch } from 'lucide-react'
import { api } from '../api/client'
import type { GenomeEvolution, Genome } from '../types'

export default function StrategiesPage() {
  const [strategies, setStrategies] = useState<GenomeEvolution[]>([])
  const [loading, setLoading] = useState(true)
  const [selectedLab, setSelectedLab] = useState<string>('SafetyLab')

  useEffect(() => {
    loadStrategies()
  }, [])

  const loadStrategies = async () => {
    try {
      const data = await api.getLabStrategies()
      setStrategies(data)
    } catch (error) {
      console.error('Failed to load strategies:', error)
    } finally {
      setLoading(false)
    }
  }

  const selectedStrategy = strategies.find((s) => s.lab_name === selectedLab)

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="fade-scale-in">
        <div className="glass rounded-2xl p-8 border-2 border-white/30">
          <div className="flex items-start space-x-4">
            <div className="w-14 h-14 gradient-bg rounded-xl flex items-center justify-center shadow-lg">
              <TrendingUp className="w-7 h-7 text-white" />
            </div>
            <div className="flex-1">
              <h1 className="text-4xl font-bold bg-gradient-to-r from-gray-900 via-primary-600 to-purple-600 bg-clip-text text-transparent mb-2">
                Lab Strategy Evolution
              </h1>
              <p className="text-gray-700 text-lg">
                Track how research strategies evolve based on Judge feedback
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Lab Selector */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <button
          onClick={() => setSelectedLab('SafetyLab')}
          className={`card group cursor-pointer transition-all duration-300 ${
            selectedLab === 'SafetyLab'
              ? 'ring-4 ring-red-300 ring-offset-2 scale-105'
              : 'hover:scale-105'
          }`}
        >
          <div className="flex items-center space-x-4 mb-4">
            <div className={`w-16 h-16 rounded-xl flex items-center justify-center shadow-lg transition-all ${
              selectedLab === 'SafetyLab' 
                ? 'bg-gradient-to-br from-red-500 to-orange-600' 
                : 'bg-gray-200 group-hover:bg-gradient-to-br group-hover:from-red-400 group-hover:to-orange-500'
            }`}>
              <Shield className="w-8 h-8 text-white" />
            </div>
            <div className="text-left">
              <h2 className="text-2xl font-bold text-gray-900">SafetyLab</h2>
              <p className="text-xs text-gray-500 font-medium">COLLISION AVOIDANCE</p>
            </div>
          </div>
          <p className="text-sm text-gray-600 text-left">
            Focus on robustness, safety guarantees, and rare events
          </p>
        </button>

        <button
          onClick={() => setSelectedLab('PerformanceLab')}
          className={`card group cursor-pointer transition-all duration-300 ${
            selectedLab === 'PerformanceLab'
              ? 'ring-4 ring-blue-300 ring-offset-2 scale-105'
              : 'hover:scale-105'
          }`}
        >
          <div className="flex items-center space-x-4 mb-4">
            <div className={`w-16 h-16 rounded-xl flex items-center justify-center shadow-lg transition-all ${
              selectedLab === 'PerformanceLab' 
                ? 'bg-gradient-to-br from-blue-500 to-blue-600' 
                : 'bg-gray-200 group-hover:bg-gradient-to-br group-hover:from-blue-400 group-hover:to-blue-500'
            }`}>
              <Zap className="w-8 h-8 text-white" />
            </div>
            <div className="text-left">
              <h2 className="text-2xl font-bold text-gray-900">PerformanceLab</h2>
              <p className="text-xs text-gray-500 font-medium">EFFICIENCY OPTIMIZATION</p>
            </div>
          </div>
          <p className="text-sm text-gray-600 text-left">
            Focus on SOTA metrics, speed, and computational efficiency
          </p>
        </button>
      </div>

      {/* Evolution Timeline */}
      {selectedStrategy && selectedStrategy.versions.length > 0 ? (
        <div className="card slide-in">
          <div className="flex items-center space-x-3 mb-6">
            <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${
              selectedLab === 'SafetyLab' ? 'bg-red-100' : 'bg-blue-100'
            }`}>
              <TrendingUp className={`w-5 h-5 ${
                selectedLab === 'SafetyLab' ? 'text-red-600' : 'text-blue-600'
              }`} />
            </div>
            <h3 className="text-xl font-bold text-gray-900">Evolution Timeline</h3>
            <span className="px-3 py-1 bg-gray-100 text-gray-700 text-sm font-medium rounded-full">
              {selectedStrategy.versions.length} version{selectedStrategy.versions.length !== 1 ? 's' : ''}
            </span>
          </div>

          <div className="space-y-6">
            {selectedStrategy.versions.map((genome, idx) => (
              <GenomeVersionCard
                key={genome.id}
                genome={genome}
                isLatest={idx === selectedStrategy.versions.length - 1}
                labColor={selectedLab === 'SafetyLab' ? 'safety' : 'performance'}
              />
            ))}
          </div>
        </div>
      ) : (
        <div className="card text-center py-16 slide-in">
          <div className="float">
            <GitBranch className="w-20 h-20 text-gray-300 mx-auto mb-4" />
          </div>
          <h3 className="text-2xl font-bold text-gray-900 mb-2">No Strategy Evolution Yet</h3>
          <p className="text-gray-600 mb-8 text-lg max-w-2xl mx-auto">
            {selectedLab} strategies will evolve as you run analyses and the Judge provides feedback. 
            Start by analyzing events in your datasets to see strategies improve over time!
          </p>
          <div className="bg-gradient-to-br from-primary-50 to-purple-50 rounded-xl p-6 max-w-2xl mx-auto border-2 border-primary-200">
            <h4 className="font-bold text-gray-900 mb-3">How Strategy Evolution Works</h4>
            <div className="space-y-2 text-sm text-gray-700 text-left">
              <p>• <strong>1. Analyze Events:</strong> Run analysis on driving events</p>
              <p>• <strong>2. Labs Compete:</strong> SafetyLab and PerformanceLab propose strategies</p>
              <p>• <strong>3. Judge Evaluates:</strong> Impartial AI judges which approach is better</p>
              <p>• <strong>4. Evolution:</strong> Winning strategies influence future versions</p>
              <p>• <strong>5. Continuous Improvement:</strong> System learns and adapts over time</p>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

interface GenomeVersionCardProps {
  genome: Genome
  isLatest: boolean
  labColor: 'safety' | 'performance'
}

function GenomeVersionCard({ genome, isLatest, labColor }: GenomeVersionCardProps) {
  const [expanded, setExpanded] = useState(isLatest)

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    })
  }

  return (
    <div className={`border-l-4 ${labColor === 'safety' ? 'border-safety-500' : 'border-performance-500'} pl-6 pb-6 relative`}>
      {/* Timeline dot */}
      <div className={`absolute left-0 top-0 w-4 h-4 rounded-full -ml-2 ${labColor === 'safety' ? 'bg-safety-500' : 'bg-performance-500'}`} />

      <div className="bg-white rounded-lg border border-gray-200 p-4">
        <div className="flex items-start justify-between mb-3">
          <div className="flex items-center space-x-3">
            <h4 className="text-lg font-semibold text-gray-900">{genome.version}</h4>
            {isLatest && (
              <span className="px-2 py-1 bg-primary-100 text-primary-700 text-xs font-medium rounded">
                Latest
              </span>
            )}
            {genome.parent_version && (
              <span className="text-sm text-gray-500 flex items-center">
                <GitBranch className="w-3 h-3 mr-1" />
                from {genome.parent_version}
              </span>
            )}
          </div>
          <button
            onClick={() => setExpanded(!expanded)}
            className="text-sm text-primary-600 hover:text-primary-700 font-medium"
          >
            {expanded ? 'Hide Details' : 'Show Details'}
          </button>
        </div>

        <p className="text-sm text-gray-600 mb-2">{genome.change_description}</p>
        <p className="text-xs text-gray-500">{formatDate(genome.created_at)}</p>

        {expanded && (
          <div className="mt-4 pt-4 border-t border-gray-200 space-y-4">
            {/* Keywords */}
            <div>
              <h5 className="text-sm font-semibold text-gray-900 mb-2">Keywords</h5>
              <div className="flex flex-wrap gap-2">
                {genome.genome_data.retrieval_preferences.keywords.map((keyword, idx) => (
                  <span
                    key={idx}
                    className={`px-2 py-1 ${labColor === 'safety' ? 'bg-safety-100 text-safety-700' : 'bg-performance-100 text-performance-700'} text-xs rounded`}
                  >
                    {keyword}
                  </span>
                ))}
              </div>
            </div>

            {/* Critique Dimensions */}
            <div>
              <h5 className="text-sm font-semibold text-gray-900 mb-2">Critique Focus</h5>
              <div className="space-y-2">
                {Object.entries(genome.genome_data.critique_focus.weights).map(([dim, weight]) => (
                  <div key={dim} className="flex items-center justify-between text-sm">
                    <span className="text-gray-700 capitalize">{dim.replace(/_/g, ' ')}</span>
                    <div className="flex items-center space-x-2">
                      <div className="w-32 h-2 bg-gray-200 rounded-full overflow-hidden">
                        <div
                          className={`h-full ${labColor === 'safety' ? 'bg-safety-500' : 'bg-performance-500'}`}
                          style={{ width: `${(weight as number) * 100}%` }}
                        />
                      </div>
                      <span className="text-gray-600 font-medium w-12 text-right">
                        {((weight as number) * 100).toFixed(0)}%
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Venue Weights */}
            <div>
              <h5 className="text-sm font-semibold text-gray-900 mb-2">Venue Preferences</h5>
              <div className="grid grid-cols-2 gap-2">
                {Object.entries(genome.genome_data.retrieval_preferences.venue_weights)
                  .sort(([, a], [, b]) => (b as number) - (a as number))
                  .map(([venue, weight]) => (
                    <div key={venue} className="flex items-center justify-between text-sm bg-gray-50 rounded px-3 py-2">
                      <span className="font-medium text-gray-700">{venue}</span>
                      <span className="text-gray-600">{((weight as number) * 100).toFixed(0)}%</span>
                    </div>
                  ))}
              </div>
            </div>

            {/* Year Window */}
            <div>
              <h5 className="text-sm font-semibold text-gray-900 mb-2">Year Window</h5>
              <div className="text-sm text-gray-700">
                {genome.genome_data.retrieval_preferences.year_window[0]} -{' '}
                {genome.genome_data.retrieval_preferences.year_window[1]}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
