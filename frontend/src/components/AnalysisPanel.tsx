import { Shield, Zap, Scale, TrendingUp, Award, CheckCircle } from 'lucide-react'
import { useState, useEffect } from 'react'
import type { Analysis } from '../types'

interface AnalysisPanelProps {
  analysis: Analysis | null
  loading: boolean
}

export default function AnalysisPanel({ analysis, loading }: AnalysisPanelProps) {
  if (loading) {
    return (
      <div className="card">
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <div className="relative mb-6">
              <div className="animate-spin rounded-full h-16 w-16 border-4 border-primary-200 mx-auto"></div>
              <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-primary-600 absolute top-0 left-1/2 transform -translate-x-1/2"></div>
            </div>
            <p className="text-xl font-bold text-gray-900 mb-2">Running multi-agent analysis...</p>
            <p className="text-sm text-gray-600 mb-4">SafetyLab and PerformanceLab are analyzing the scenario</p>
            <div className="flex justify-center space-x-4">
              <div className="flex items-center space-x-2 bg-safety-50 px-4 py-2 rounded-lg">
                <Shield className="w-4 h-4 text-safety-600 animate-pulse" />
                <span className="text-sm font-medium text-safety-700">SafetyLab</span>
              </div>
              <div className="flex items-center space-x-2 bg-performance-50 px-4 py-2 rounded-lg">
                <Zap className="w-4 h-4 text-performance-600 animate-pulse" />
                <span className="text-sm font-medium text-performance-700">PerformanceLab</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    )
  }

  if (!analysis) {
    return (
      <div className="card">
        <div className="text-center py-16">
          <div className="float">
            <Scale className="w-20 h-20 text-primary-400 mx-auto mb-4" />
          </div>
          <h3 className="text-2xl font-bold text-gray-900 mb-2">No Analysis Yet</h3>
          <p className="text-gray-600 text-lg">
            Click "Run Analysis" to start the multi-agent research process
          </p>
        </div>
      </div>
    )
  }

  const { safety_lab_output, performance_lab_output, judge_decision } = analysis

  const getWinnerColor = (winner: string) => {
    if (winner === 'SafetyLab') return 'text-safety-600'
    if (winner === 'PerformanceLab') return 'text-performance-600'
    return 'text-gray-600'
  }

  const getWinnerBg = (winner: string) => {
    if (winner === 'SafetyLab') return 'bg-safety-50 border-safety-200'
    if (winner === 'PerformanceLab') return 'bg-performance-50 border-performance-200'
    return 'bg-gray-50 border-gray-200'
  }

  return (
    <div className="space-y-6">
      {/* Judge Decision */}
      <div className={`card border-2 ${getWinnerBg(judge_decision.winner)} fade-scale-in relative overflow-hidden`}>
        {/* Animated background effect */}
        <div className="absolute top-0 right-0 w-64 h-64 bg-gradient-to-br from-primary-200/20 to-purple-200/20 rounded-full blur-3xl"></div>
        
        <div className="relative z-10">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center space-x-3">
              <div className="w-12 h-12 gradient-bg rounded-xl flex items-center justify-center shadow-lg">
                <Award className="w-6 h-6 text-white" />
              </div>
              <h3 className="text-2xl font-bold text-gray-900">Judge Decision</h3>
            </div>
            <div className={`px-6 py-3 rounded-xl font-bold text-lg shadow-lg ${getWinnerColor(judge_decision.winner)} bg-white border-2 border-current flex items-center space-x-2`}>
              <CheckCircle className="w-5 h-5" />
              <span>Winner: {judge_decision.winner}</span>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-6 mb-6">
            <AnimatedScoreCard
              icon={<Shield className="w-6 h-6 text-white" />}
              label="SafetyLab"
              score={judge_decision.safety_lab_score}
              color="safety"
              isWinner={judge_decision.winner === 'SafetyLab'}
            />
            <AnimatedScoreCard
              icon={<Zap className="w-6 h-6 text-white" />}
              label="PerformanceLab"
              score={judge_decision.performance_lab_score}
              color="performance"
              isWinner={judge_decision.winner === 'PerformanceLab'}
            />
          </div>

          <div className="bg-white/80 backdrop-blur-sm rounded-xl p-6 border-2 border-gray-200">
            <h4 className="font-bold text-gray-900 mb-3 text-lg">Reasoning</h4>
            <p className="text-gray-700 leading-relaxed">{judge_decision.reasoning}</p>
          </div>
        </div>
      </div>

      {/* Lab Outputs Side by Side */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* SafetyLab Output */}
        <div className="card border-2 border-safety-200 slide-in stagger-1" style={{ animationFillMode: 'both' }}>
          <div className="flex items-center space-x-3 mb-6">
            <div className="w-10 h-10 bg-gradient-to-br from-safety-500 to-safety-600 rounded-lg flex items-center justify-center shadow-md">
              <Shield className="w-5 h-5 text-white" />
            </div>
            <h3 className="text-xl font-bold text-gray-900">SafetyLab</h3>
          </div>

          <LabOutputContent output={safety_lab_output} color="safety" />

          {/* Strengths & Weaknesses */}
          <div className="mt-4 pt-4 border-t border-gray-200 space-y-3">
            <div>
              <h5 className="text-sm font-semibold text-green-700 mb-1">Strengths</h5>
              <ul className="text-sm text-gray-700 space-y-1">
                {judge_decision.safety_lab_strengths.map((strength, idx) => (
                  <li key={idx} className="flex items-start">
                    <span className="text-green-500 mr-2">✓</span>
                    <span>{strength}</span>
                  </li>
                ))}
              </ul>
            </div>
            <div>
              <h5 className="text-sm font-semibold text-red-700 mb-1">Weaknesses</h5>
              <ul className="text-sm text-gray-700 space-y-1">
                {judge_decision.safety_lab_weaknesses.map((weakness, idx) => (
                  <li key={idx} className="flex items-start">
                    <span className="text-red-500 mr-2">✗</span>
                    <span>{weakness}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>

        {/* PerformanceLab Output */}
        <div className="card border-2 border-performance-200 slide-in stagger-2" style={{ animationFillMode: 'both' }}>
          <div className="flex items-center space-x-3 mb-6">
            <div className="w-10 h-10 bg-gradient-to-br from-performance-500 to-performance-600 rounded-lg flex items-center justify-center shadow-md">
              <Zap className="w-5 h-5 text-white" />
            </div>
            <h3 className="text-xl font-bold text-gray-900">PerformanceLab</h3>
          </div>

          <LabOutputContent output={performance_lab_output} color="performance" />

          {/* Strengths & Weaknesses */}
          <div className="mt-4 pt-4 border-t border-gray-200 space-y-3">
            <div>
              <h5 className="text-sm font-semibold text-green-700 mb-1">Strengths</h5>
              <ul className="text-sm text-gray-700 space-y-1">
                {judge_decision.performance_lab_strengths.map((strength, idx) => (
                  <li key={idx} className="flex items-start">
                    <span className="text-green-500 mr-2">✓</span>
                    <span>{strength}</span>
                  </li>
                ))}
              </ul>
            </div>
            <div>
              <h5 className="text-sm font-semibold text-red-700 mb-1">Weaknesses</h5>
              <ul className="text-sm text-gray-700 space-y-1">
                {judge_decision.performance_lab_weaknesses.map((weakness, idx) => (
                  <li key={idx} className="flex items-start">
                    <span className="text-red-500 mr-2">✗</span>
                    <span>{weakness}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </div>

      {/* Genome Updates */}
      {(analysis.new_safety_genome_version || analysis.new_performance_genome_version) && (
        <div className="card bg-gradient-to-br from-primary-50 to-purple-50 border-2 border-primary-300 slide-in stagger-3" style={{ animationFillMode: 'both' }}>
          <div className="flex items-center space-x-3 mb-6">
            <div className="w-10 h-10 gradient-bg rounded-lg flex items-center justify-center shadow-md">
              <TrendingUp className="w-5 h-5 text-white" />
            </div>
            <h3 className="text-xl font-bold text-gray-900">Strategy Evolution</h3>
          </div>
          <div className="space-y-3">
            {analysis.new_safety_genome_version && (
              <div className="bg-white rounded-xl p-4 border-2 border-safety-200 shadow-md">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-safety-600 text-lg">SafetyLab:</span>
                  <div className="flex items-center space-x-2">
                    <span className="font-mono text-gray-600">{analysis.safety_genome_version}</span>
                    <span className="text-gray-400">→</span>
                    <span className="font-mono font-bold text-safety-600">{analysis.new_safety_genome_version}</span>
                  </div>
                </div>
              </div>
            )}
            {analysis.new_performance_genome_version && (
              <div className="bg-white rounded-xl p-4 border-2 border-performance-200 shadow-md">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-performance-600 text-lg">PerformanceLab:</span>
                  <div className="flex items-center space-x-2">
                    <span className="font-mono text-gray-600">{analysis.performance_genome_version}</span>
                    <span className="text-gray-400">→</span>
                    <span className="font-mono font-bold text-performance-600">{analysis.new_performance_genome_version}</span>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}

interface AnimatedScoreCardProps {
  icon: React.ReactNode
  label: string
  score: number
  color: 'safety' | 'performance'
  isWinner: boolean
}

function AnimatedScoreCard({ icon, label, score, color, isWinner }: AnimatedScoreCardProps) {
  const [displayScore, setDisplayScore] = useState(0)
  
  useEffect(() => {
    const duration = 1500
    const steps = 60
    const increment = score / steps
    let current = 0
    
    const timer = setInterval(() => {
      current += increment
      if (current >= score) {
        setDisplayScore(score)
        clearInterval(timer)
      } else {
        setDisplayScore(current)
      }
    }, duration / steps)
    
    return () => clearInterval(timer)
  }, [score])
  
  const bgColor = color === 'safety' ? 'from-safety-500 to-safety-600' : 'from-performance-500 to-performance-600'
  const percentage = Math.round(displayScore * 100)
  
  return (
    <div className={`bg-white rounded-xl p-6 border-2 ${color === 'safety' ? 'border-safety-200' : 'border-performance-200'} shadow-lg relative overflow-hidden ${
      isWinner ? 'ring-4 ring-yellow-400 ring-offset-2' : ''
    }`}>
      {isWinner && (
        <div className="absolute top-2 right-2">
          <div className="w-8 h-8 bg-yellow-400 rounded-full flex items-center justify-center animate-bounce">
            <Award className="w-5 h-5 text-yellow-900" />
          </div>
        </div>
      )}
      <div className={`w-14 h-14 bg-gradient-to-br ${bgColor} rounded-xl flex items-center justify-center shadow-lg mb-4`}>
        {icon}
      </div>
      <div className="mb-2">
        <span className="font-bold text-gray-900 text-lg">{label}</span>
      </div>
      <div className="text-5xl font-black bg-gradient-to-r ${bgColor} bg-clip-text text-transparent mb-3">
        {percentage}%
      </div>
      <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
        <div 
          className={`h-full bg-gradient-to-r ${bgColor} transition-all duration-1000 ease-out rounded-full`}
          style={{ width: `${percentage}%` }}
        >
          <div className="w-full h-full shimmer"></div>
        </div>
      </div>
    </div>
  )
}

interface LabOutputContentProps {
  output: any
  color: 'safety' | 'performance'
}

function LabOutputContent({ output, color }: LabOutputContentProps) {
  const synthesis = output.synthesis
  
  // Define color classes to avoid dynamic Tailwind class generation issues
  const bulletColor = color === 'safety' ? 'text-safety-500' : 'text-performance-500'
  const scoreColor = color === 'safety' ? 'text-safety-600' : 'text-performance-600'
  const confidenceColor = color === 'safety' ? 'text-safety-600' : 'text-performance-600'

  return (
    <div className="space-y-4">
      {/* Summary */}
      <div>
        <h4 className="text-sm font-semibold text-gray-900 mb-2">Summary</h4>
        <p className="text-sm text-gray-700">{synthesis.summary}</p>
      </div>

      {/* Key Methods */}
      <div>
        <h4 className="text-sm font-semibold text-gray-900 mb-2">Key Methods</h4>
        <ul className="space-y-1">
          {synthesis.key_methods.map((method: string, idx: number) => (
            <li key={idx} className="text-sm text-gray-700 flex items-start">
              <span className={`${bulletColor} mr-2`}>•</span>
              <span>{method}</span>
            </li>
          ))}
        </ul>
      </div>

      {/* Top Papers */}
      <div>
        <h4 className="text-sm font-semibold text-gray-900 mb-2">
          Top Papers ({synthesis.num_papers_analyzed} analyzed)
        </h4>
        <div className="space-y-2">
          {synthesis.top_papers.map((paper: any, idx: number) => (
            <div key={idx} className="bg-gray-50 rounded p-2 text-xs">
              <div className="font-medium text-gray-900 line-clamp-1">{paper.title}</div>
              <div className="flex items-center justify-between mt-1">
                <span className="text-gray-500">{paper.method_category}</span>
                <span className={`${scoreColor} font-semibold`}>
                  {(paper.score * 100).toFixed(0)}%
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Confidence */}
      <div className="flex items-center justify-between text-sm">
        <span className="text-gray-600">Confidence Level</span>
        <span className={`font-semibold capitalize ${confidenceColor}`}>
          {synthesis.confidence_level}
        </span>
      </div>
    </div>
  )
}
