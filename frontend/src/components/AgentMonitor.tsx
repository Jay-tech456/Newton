import { useState, useEffect } from 'react'
import { Brain, FileSearch, Lightbulb, CheckCircle, Clock, Activity, Zap } from 'lucide-react'

interface AgentActivity {
  id: string
  agent: string
  action: string
  status: 'running' | 'completed' | 'pending'
  timestamp: Date
  details?: string
  progress?: number
}

interface AgentMonitorProps {
  datasetId?: number
  eventId?: number
  isAnalyzing: boolean
}

export default function AgentMonitor({ datasetId, eventId, isAnalyzing }: AgentMonitorProps) {
  const [activities, setActivities] = useState<AgentActivity[]>([])
  const [currentAgent, setCurrentAgent] = useState<string>('')

  useEffect(() => {
    if (isAnalyzing) {
      simulateAgentActivity()
    }
  }, [isAnalyzing, datasetId, eventId])

  const simulateAgentActivity = () => {
    // Simulate real-time agent activities
    const agentSequence = [
      { agent: 'Reader', action: 'Extracting event data from dataset', duration: 2000 },
      { agent: 'Reader', action: 'Analyzing telemetry patterns', duration: 1500 },
      { agent: 'Retriever', action: 'Searching research papers on arXiv', duration: 3000 },
      { agent: 'Retriever', action: 'Querying Semantic Scholar database', duration: 2500 },
      { agent: 'Critic', action: 'Evaluating event severity and risk factors', duration: 2000 },
      { agent: 'Critic', action: 'Identifying safety implications', duration: 1800 },
      { agent: 'Planner', action: 'Generating research hypotheses', duration: 2200 },
      { agent: 'Planner', action: 'Designing experiment protocols', duration: 2500 },
      { agent: 'Synthesizer', action: 'Combining insights from all agents', duration: 2000 },
      { agent: 'Synthesizer', action: 'Generating final analysis report', duration: 1500 },
    ]

    let delay = 0

    agentSequence.forEach((step, index) => {
      setTimeout(() => {
        const activity: AgentActivity = {
          id: `activity-${index}`,
          agent: step.agent,
          action: step.action,
          status: 'running',
          timestamp: new Date(),
          progress: 0
        }
        
        setActivities(prev => [...prev, activity])
        setCurrentAgent(step.agent)

        // Simulate progress
        const progressInterval = setInterval(() => {
          setActivities(prev => prev.map(a => 
            a.id === activity.id && a.progress !== undefined && a.progress < 100
              ? { ...a, progress: Math.min(100, a.progress + 10) }
              : a
          ))
        }, step.duration / 10)

        // Mark as completed
        setTimeout(() => {
          clearInterval(progressInterval)
          setActivities(prev => prev.map(a => 
            a.id === activity.id 
              ? { ...a, status: 'completed' as const, progress: 100 }
              : a
          ))
        }, step.duration)
      }, delay)

      delay += step.duration
    })
  }

  const getAgentIcon = (agent: string) => {
    switch (agent) {
      case 'Reader':
        return <FileSearch className="w-5 h-5" />
      case 'Retriever':
        return <Activity className="w-5 h-5" />
      case 'Critic':
        return <Zap className="w-5 h-5" />
      case 'Planner':
        return <Lightbulb className="w-5 h-5" />
      case 'Synthesizer':
        return <Brain className="w-5 h-5" />
      default:
        return <Activity className="w-5 h-5" />
    }
  }

  const getAgentColor = (agent: string) => {
    switch (agent) {
      case 'Reader':
        return 'text-blue-600 bg-blue-50'
      case 'Retriever':
        return 'text-purple-600 bg-purple-50'
      case 'Critic':
        return 'text-red-600 bg-red-50'
      case 'Planner':
        return 'text-green-600 bg-green-50'
      case 'Synthesizer':
        return 'text-orange-600 bg-orange-50'
      default:
        return 'text-gray-600 bg-gray-50'
    }
  }

  return (
    <div className="h-full flex flex-col bg-white rounded-lg shadow-sm border border-gray-200">
      {/* Header */}
      <div className="px-6 py-4 border-b border-gray-200">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-semibold text-gray-900">Agent Activity Monitor</h2>
          {isAnalyzing && (
            <div className="flex items-center space-x-2 text-sm text-green-600">
              <div className="w-2 h-2 bg-green-600 rounded-full animate-pulse"></div>
              <span>Active</span>
            </div>
          )}
        </div>
        {currentAgent && (
          <p className="text-sm text-gray-600 mt-1">
            Current: <span className="font-medium">{currentAgent}</span>
          </p>
        )}
      </div>

      {/* Activity Feed */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {activities.length === 0 ? (
          <div className="text-center py-12">
            <Brain className="w-12 h-12 text-gray-300 mx-auto mb-3" />
            <p className="text-gray-500 text-sm">
              {isAnalyzing ? 'Initializing agents...' : 'No agent activity yet'}
            </p>
            <p className="text-gray-400 text-xs mt-1">
              Click "Run Analysis" to start
            </p>
          </div>
        ) : (
          activities.map((activity) => (
            <div
              key={activity.id}
              className="flex items-start space-x-3 p-4 rounded-lg border border-gray-100 hover:border-gray-200 transition-colors"
            >
              {/* Agent Icon */}
              <div className={`p-2 rounded-lg ${getAgentColor(activity.agent)}`}>
                {getAgentIcon(activity.agent)}
              </div>

              {/* Activity Details */}
              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between mb-1">
                  <h3 className="text-sm font-medium text-gray-900">
                    {activity.agent}
                  </h3>
                  <div className="flex items-center space-x-2">
                    {activity.status === 'running' && (
                      <Clock className="w-4 h-4 text-blue-500 animate-spin" />
                    )}
                    {activity.status === 'completed' && (
                      <CheckCircle className="w-4 h-4 text-green-500" />
                    )}
                  </div>
                </div>
                
                <p className="text-sm text-gray-600 mb-2">{activity.action}</p>
                
                {/* Progress Bar */}
                {activity.status === 'running' && activity.progress !== undefined && (
                  <div className="w-full bg-gray-200 rounded-full h-1.5">
                    <div
                      className="bg-blue-600 h-1.5 rounded-full transition-all duration-300"
                      style={{ width: `${activity.progress}%` }}
                    ></div>
                  </div>
                )}

                {activity.details && (
                  <p className="text-xs text-gray-500 mt-2">{activity.details}</p>
                )}

                <p className="text-xs text-gray-400 mt-1">
                  {activity.timestamp.toLocaleTimeString()}
                </p>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Summary Footer */}
      {activities.length > 0 && (
        <div className="px-6 py-4 border-t border-gray-200 bg-gray-50">
          <div className="flex items-center justify-between text-sm">
            <span className="text-gray-600">
              {activities.filter(a => a.status === 'completed').length} / {activities.length} tasks completed
            </span>
            {activities.every(a => a.status === 'completed') && (
              <span className="text-green-600 font-medium flex items-center space-x-1">
                <CheckCircle className="w-4 h-4" />
                <span>Analysis Complete</span>
              </span>
            )}
          </div>
        </div>
      )}
    </div>
  )
}
