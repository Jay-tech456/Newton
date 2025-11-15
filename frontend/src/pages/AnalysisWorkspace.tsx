import { useState, useEffect, useRef } from 'react'
import { useParams, Link } from 'react-router-dom'
import { ArrowLeft, Send, Bot, User, Sparkles, Activity, CheckCircle, Clock, Loader, AlertTriangle, TrendingUp } from 'lucide-react'
import { api } from '../api/client'
import type { Dataset, Event, Analysis } from '../types'
import VideoPlayer from '../components/VideoPlayer'
import EventTimeline from '../components/EventTimeline'

interface Message {
  id: number
  role: 'user' | 'assistant' | 'system'
  content: string
  timestamp: Date
}

interface TaskStep {
  id: number
  title: string
  status: 'pending' | 'in_progress' | 'completed'
  details?: string
}

export default function AnalysisWorkspace() {
  const { datasetId } = useParams<{ datasetId: string }>()
  const [dataset, setDataset] = useState<Dataset | null>(null)
  const [events, setEvents] = useState<Event[]>([])
  const [selectedEvent, setSelectedEvent] = useState<Event | null>(null)
  const [analysis, setAnalysis] = useState<Analysis | null>(null)
  const [loading, setLoading] = useState(true)
  const [analyzing, setAnalyzing] = useState(false)
  
  // Chat state
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 1,
      role: 'system',
      content: 'Welcome to AutoLab Drive! I\'m your AI assistant. Ask me to analyze events, explain findings, or suggest improvements.',
      timestamp: new Date()
    }
  ])
  const [inputMessage, setInputMessage] = useState('')
  const [isTyping, setIsTyping] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  
  // Task execution state
  const [taskSteps, setTaskSteps] = useState<TaskStep[]>([])

  const handleEventSelect = (event: Event) => {
    setSelectedEvent(event)
    addSystemMessage(`Selected event: ${event.event_type.replace(/_/g, ' ')} at ${event.start_timestamp.toFixed(1)}s`)
  }

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'high':
        return 'bg-red-100 text-red-800 border-red-300'
      case 'medium':
        return 'bg-yellow-100 text-yellow-800 border-yellow-300'
      case 'low':
        return 'bg-green-100 text-green-800 border-green-300'
      default:
        return 'bg-gray-100 text-gray-800 border-gray-300'
    }
  }

  useEffect(() => {
    if (datasetId) {
      loadDatasetAndEvents(parseInt(datasetId))
    }
  }, [datasetId])

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const loadDatasetAndEvents = async (id: number) => {
    try {
      const [datasetData, eventsData] = await Promise.all([
        api.getDataset(id),
        api.getDatasetEvents(id),
      ])
      setDataset(datasetData)
      setEvents(eventsData)
      
      // Add welcome message with dataset info
      if (eventsData.length === 0) {
        addSystemMessage(`Loaded dataset "${datasetData.name}" but no events were detected.`)
        addAssistantMessage(
          `⚠️ No events detected in this dataset.\n\nThis could mean:\n• The telemetry data doesn't contain event triggers (cut_in_flag, pedestrian_flag, etc.)\n• The driving conditions were too normal to trigger detection rules\n• The dataset may need proper telemetry format\n\n📋 Required telemetry columns:\n- frame_id, timestamp, ego_speed_mps\n- ego_yaw, lead_distance_m\n- road_type, weather\n- cut_in_flag, pedestrian_flag\n\nTry uploading one of the demo datasets from the backend/storage/datasets/demos/ folder for a working example!`
        )
      } else {
        addSystemMessage(`Loaded dataset "${datasetData.name}" with ${eventsData.length} events detected.`)
      }
    } catch (error) {
      console.error('Failed to load dataset:', error)
      addSystemMessage('Error loading dataset. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const addSystemMessage = (content: string) => {
    setMessages(prev => [...prev, {
      id: Date.now(),
      role: 'system',
      content,
      timestamp: new Date()
    }])
  }

  const addAssistantMessage = (content: string) => {
    setMessages(prev => [...prev, {
      id: Date.now(),
      role: 'assistant',
      content,
      timestamp: new Date()
    }])
  }

  const handleSendMessage = async () => {
    if (!inputMessage.trim()) return

    const userMessage: Message = {
      id: Date.now(),
      role: 'user',
      content: inputMessage,
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setInputMessage('')
    setIsTyping(true)

    // Simulate AI response based on user input
    setTimeout(() => {
      handleUserQuery(userMessage.content)
      setIsTyping(false)
    }, 1000)
  }

  const handleUserQuery = async (query: string) => {
    const lowerQuery = query.toLowerCase()

    if (lowerQuery.includes('analyze') || lowerQuery.includes('run analysis')) {
      if (events.length === 0) {
        addAssistantMessage('No events detected in this dataset. Please upload a dataset with events first.')
        return
      }
      
      addAssistantMessage(`Starting analysis on ${events.length} detected events. I'll process each event through SafetyLab and PerformanceLab...`)
      await runAnalysis()
    } else if (lowerQuery.includes('event') || lowerQuery.includes('what happened')) {
      if (events.length > 0) {
        const eventList = events.map(e => `- ${e.event_type.replace(/_/g, ' ')} at ${e.start_timestamp.toFixed(1)}s (${e.severity} severity)`).join('\n')
        addAssistantMessage(`I detected ${events.length} events in this dataset:\n\n${eventList}\n\nWould you like me to analyze any specific event?`)
      } else {
        addAssistantMessage('No events have been detected in this dataset yet.')
      }
    } else if (lowerQuery.includes('help')) {
      addAssistantMessage(`I can help you with:\n\n• Analyzing driving events with multi-agent research\n• Explaining safety and performance insights\n• Comparing different strategies\n• Suggesting improvements\n\nTry asking: "Analyze the events" or "What events were detected?"`)
    } else {
      addAssistantMessage(`I understand you're asking about: "${query}". I'm currently focused on analyzing driving events. Try asking me to "analyze events" or type "help" for more options.`)
    }
  }

  const runAnalysis = async () => {
    if (!dataset || events.length === 0 || !selectedEvent) return

    setAnalyzing(true)
    
    // Initialize task steps with more detail
    setTaskSteps([
      { id: 1, title: '📊 Loading Event Data', status: 'in_progress', details: 'Extracting telemetry and context' },
      { id: 2, title: '🛡️ SafetyLab Analysis', status: 'pending', details: 'Prioritizing collision avoidance' },
      { id: 3, title: '⚡ PerformanceLab Analysis', status: 'pending', details: 'Optimizing efficiency' },
      { id: 4, title: '⚖️ Judge Evaluation', status: 'pending', details: 'Comparing strategies' },
      { id: 5, title: '✨ Generating Insights', status: 'pending', details: 'Compiling results' }
    ])

    try {
      // Simulate step progression
      await updateTaskStep(1, 'completed', 'Event data loaded successfully')
      await new Promise(resolve => setTimeout(resolve, 500))
      
      await updateTaskStep(2, 'in_progress')
      await new Promise(resolve => setTimeout(resolve, 1500))
      await updateTaskStep(2, 'completed', 'Safety analysis complete')
      
      await updateTaskStep(3, 'in_progress')
      await new Promise(resolve => setTimeout(resolve, 1500))
      await updateTaskStep(3, 'completed', 'Performance analysis complete')
      
      await updateTaskStep(4, 'in_progress')
      const analysisData = await api.analyzeEvent(dataset.id, events[0].id)
      setAnalysis(analysisData)
      await updateTaskStep(4, 'completed', 'Judge decision rendered')
      
      await updateTaskStep(5, 'in_progress')
      await new Promise(resolve => setTimeout(resolve, 500))
      await updateTaskStep(5, 'completed', 'Analysis complete')
      
      addAssistantMessage(`Analysis complete! The judge has evaluated both labs. Winner: ${analysisData.judge_decision.winner}. Check the results panel for detailed insights.`)
    } catch (error) {
      console.error('Analysis failed:', error)
      addAssistantMessage('Analysis failed. Please try again.')
    } finally {
      setAnalyzing(false)
    }
  }

  const updateTaskStep = async (id: number, status: TaskStep['status'], details?: string) => {
    setTaskSteps(prev => prev.map(step => 
      step.id === id ? { ...step, status, details } : step
    ))
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="relative">
          <div className="animate-spin rounded-full h-16 w-16 border-4 border-primary-200"></div>
          <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-primary-600 absolute top-0"></div>
        </div>
      </div>
    )
  }

  if (!dataset) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-600">Dataset not found</p>
      </div>
    )
  }

  return (
    <div className="h-screen flex flex-col">
      {/* Header */}
      <div className="glass border-b border-white/20 px-6 py-4 relative z-10">
        <Link to="/" className="inline-flex items-center text-primary-600 hover:text-primary-700 mb-2 font-medium transition-all hover:scale-105">
          <ArrowLeft className="w-4 h-4 mr-2" />
          Back to Datasets
        </Link>
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold bg-gradient-to-r from-gray-900 via-primary-600 to-purple-600 bg-clip-text text-transparent">
              {dataset.name}
            </h1>
            <div className="flex items-center space-x-4 mt-1 text-sm text-gray-600">
              <span>{dataset.frame_count.toLocaleString()} frames</span>
              <span>{Math.floor(dataset.duration_seconds / 60)}:{(dataset.duration_seconds % 60).toString().padStart(2, '0')}</span>
              <span>{events.length} events</span>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content - Split View */}
      <div className="flex-1 flex overflow-hidden">
        {/* Left Panel - Video & Events */}
        <div className="w-1/2 flex flex-col border-r border-gray-200 bg-white overflow-y-auto">
          {/* Event Timeline */}
          <div className="border-b border-gray-200 p-4">
            <h2 className="text-lg font-semibold text-gray-900 mb-3">Event Timeline</h2>
            {events.length > 0 ? (
              <EventTimeline
                events={events}
                selectedEvent={selectedEvent}
                onEventSelect={handleEventSelect}
                duration={dataset.duration_seconds}
              />
            ) : (
              <div className="text-center py-8 text-gray-500">
                <p>No events detected in this dataset</p>
              </div>
            )}
          </div>

          {/* Video Player */}
          {selectedEvent && (
            <div className="p-4 border-b border-gray-200">
              <h2 className="text-lg font-semibold text-gray-900 mb-3">Event Playback</h2>
              <VideoPlayer
                datasetId={dataset.id}
                frameCount={dataset.frame_count}
                duration={dataset.duration_seconds}
                startFrame={Math.floor(selectedEvent.start_timestamp * (dataset.frame_count / dataset.duration_seconds))}
                endFrame={Math.floor(selectedEvent.end_timestamp * (dataset.frame_count / dataset.duration_seconds))}
                autoPlay={false}
              />
            </div>
          )}

          {/* Event Details */}
          {selectedEvent && (
            <div className="p-4">
              <div className="bg-gradient-to-br from-primary-50 to-purple-50 rounded-xl p-4 border-2 border-primary-200">
                <div className="flex items-center justify-between mb-3">
                  <h3 className="text-lg font-bold text-gray-900">Event Details</h3>
                  <div className={`px-4 py-2 rounded-full text-sm font-bold border-2 ${getSeverityColor(selectedEvent.severity)} shadow-md`}>
                    {selectedEvent.severity.toUpperCase()}
                  </div>
                </div>
                <div className="flex items-center space-x-3 mb-3">
                  <div className="w-10 h-10 bg-gradient-to-br from-orange-500 to-red-600 rounded-lg flex items-center justify-center shadow-md">
                    <AlertTriangle className="w-5 h-5 text-white" />
                  </div>
                  <p className="text-lg font-bold text-gray-900">
                    {selectedEvent.event_type.replace(/_/g, ' ').toUpperCase()}
                  </p>
                </div>
                <p className="text-sm text-gray-700 mb-4">{selectedEvent.description}</p>
                
                <div className="space-y-2 text-sm">
                  <div className="bg-white rounded-lg p-3 flex justify-between items-center border border-gray-200">
                    <span className="text-gray-600 font-medium">Time Range</span>
                    <span className="font-bold text-primary-600">
                      {selectedEvent.start_timestamp.toFixed(1)}s - {selectedEvent.end_timestamp.toFixed(1)}s
                    </span>
                  </div>
                  {selectedEvent.ego_speed_mps && (
                    <div className="bg-white rounded-lg p-3 flex justify-between items-center border border-gray-200">
                      <span className="text-gray-600 font-medium">Ego Speed</span>
                      <span className="font-bold text-purple-600">{selectedEvent.ego_speed_mps.toFixed(1)} m/s</span>
                    </div>
                  )}
                  {selectedEvent.weather && (
                    <div className="bg-white rounded-lg p-3 flex justify-between items-center border border-gray-200">
                      <span className="text-gray-600 font-medium">Weather</span>
                      <span className="font-bold text-blue-600 capitalize">{selectedEvent.weather}</span>
                    </div>
                  )}
                  {selectedEvent.road_type && (
                    <div className="bg-white rounded-lg p-3 flex justify-between items-center border border-gray-200">
                      <span className="text-gray-600 font-medium">Road Type</span>
                      <span className="font-bold text-green-600 capitalize">{selectedEvent.road_type}</span>
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Right Panel - Chat & Agent Tasks */}
        <div className="w-1/2 flex flex-col bg-gradient-to-br from-gray-50 via-blue-50 to-purple-50">
          {/* Chat Header */}
          <div className="glass border-b border-white/20 px-6 py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 gradient-bg rounded-xl flex items-center justify-center shadow-lg">
                  <Bot className="w-5 h-5 text-white" />
                </div>
                <div>
                  <h2 className="text-lg font-bold text-gray-900">AI Assistant & Agent Tasks</h2>
                  <p className="text-xs text-gray-600">Chat and monitor real-time execution</p>
                </div>
              </div>
              {analyzing && (
                <div className="flex items-center space-x-2 bg-green-100 px-3 py-1 rounded-full">
                  <Loader className="w-4 h-4 text-green-600 animate-spin" />
                  <span className="text-sm font-medium text-green-700">Running</span>
                </div>
              )}
            </div>
          </div>

          {/* Chat Messages - Compact */}
          <div className="max-h-64 overflow-y-auto p-4 bg-white border-b border-gray-200">
            <div className="space-y-3">
              {messages.slice(-3).map((message) => (
                <div key={message.id} className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                  <div className={`flex items-start space-x-2 max-w-[85%] ${message.role === 'user' ? 'flex-row-reverse space-x-reverse' : ''}`}>
                    <div className={`w-6 h-6 rounded-lg flex items-center justify-center flex-shrink-0 ${
                      message.role === 'user' ? 'bg-gradient-to-br from-primary-500 to-purple-600' :
                      message.role === 'system' ? 'bg-gradient-to-br from-gray-400 to-gray-500' :
                      'bg-gradient-to-br from-green-500 to-emerald-600'
                    }`}>
                      {message.role === 'user' ? <User className="w-3 h-3 text-white" /> :
                       message.role === 'system' ? <Sparkles className="w-3 h-3 text-white" /> :
                       <Bot className="w-3 h-3 text-white" />}
                    </div>
                    <div className={`rounded-lg px-3 py-2 text-xs ${
                      message.role === 'user' ? 'bg-gradient-to-br from-primary-500 to-purple-600 text-white' :
                      'bg-gray-100 text-gray-700'
                    }`}>
                      <p className="whitespace-pre-wrap">{message.content}</p>
                    </div>
                  </div>
                </div>
              ))}
              {isTyping && (
                <div className="flex justify-start">
                  <div className="flex space-x-1">
                    <div className="w-2 h-2 bg-primary-500 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-primary-500 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                    <div className="w-2 h-2 bg-primary-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>
          </div>

          {/* Action Buttons */}
          <div className="border-b border-gray-200 p-4 bg-white">
            <div className="grid grid-cols-2 gap-3">
              <button
                onClick={() => {
                  if (selectedEvent) {
                    addAssistantMessage(`Starting analysis on ${selectedEvent.event_type.replace(/_/g, ' ')} event...`)
                    runAnalysis()
                  } else {
                    addAssistantMessage('Please select an event from the timeline first!')
                  }
                }}
                disabled={analyzing || !selectedEvent}
                className="btn-primary flex items-center justify-center space-x-2 py-3 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <Activity className="w-5 h-5" />
                <span className="font-bold">Analyze Event</span>
              </button>
              
              <button
                onClick={() => {
                  addAssistantMessage('Strategy improvement will be available after analysis is complete. The winning strategy will evolve based on Judge feedback!')
                }}
                disabled={analyzing || !analysis}
                className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white font-bold py-3 px-4 rounded-lg transition-all duration-200 flex items-center justify-center space-x-2 shadow-md hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <TrendingUp className="w-5 h-5" />
                <span className="font-bold">Improve Strategy</span>
              </button>
            </div>
          </div>

          {/* Chat Input - Compact */}
          <div className="border-b border-gray-200 p-3 bg-gray-50">
            <div className="flex space-x-2">
              <input
                type="text"
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                placeholder="Ask questions..."
                className="flex-1 px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white"
                disabled={isTyping}
              />
              <button
                onClick={handleSendMessage}
                disabled={!inputMessage.trim() || isTyping}
                className="bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded-lg text-sm transition-colors disabled:opacity-50"
              >
                <Send className="w-4 h-4" />
              </button>
            </div>
          </div>

          {/* Multi-Agent Competition Visual */}
          {analyzing && taskSteps.length > 0 && (
            <div className="border-b border-gray-200 p-4 bg-gradient-to-r from-red-50 via-purple-50 to-blue-50">
              <div className="flex items-center justify-between">
                {/* SafetyLab */}
                <div className={`flex-1 text-center p-3 rounded-lg transition-all ${
                  taskSteps.find(s => s.id === 2)?.status === 'in_progress' 
                    ? 'bg-red-100 ring-2 ring-red-400 scale-105' 
                    : taskSteps.find(s => s.id === 2)?.status === 'completed'
                    ? 'bg-red-50'
                    : 'bg-white/50'
                }`}>
                  <div className="text-2xl mb-1">🛡️</div>
                  <div className="text-xs font-bold text-gray-900">SafetyLab</div>
                  {taskSteps.find(s => s.id === 2)?.status === 'completed' && (
                    <CheckCircle className="w-4 h-4 text-green-600 mx-auto mt-1" />
                  )}
                </div>

                {/* VS */}
                <div className="px-4 text-gray-400 font-bold">VS</div>

                {/* PerformanceLab */}
                <div className={`flex-1 text-center p-3 rounded-lg transition-all ${
                  taskSteps.find(s => s.id === 3)?.status === 'in_progress' 
                    ? 'bg-blue-100 ring-2 ring-blue-400 scale-105' 
                    : taskSteps.find(s => s.id === 3)?.status === 'completed'
                    ? 'bg-blue-50'
                    : 'bg-white/50'
                }`}>
                  <div className="text-2xl mb-1">⚡</div>
                  <div className="text-xs font-bold text-gray-900">PerformanceLab</div>
                  {taskSteps.find(s => s.id === 3)?.status === 'completed' && (
                    <CheckCircle className="w-4 h-4 text-green-600 mx-auto mt-1" />
                  )}
                </div>

                {/* Arrow to Judge */}
                <div className="px-2 text-gray-400">→</div>

                {/* Judge */}
                <div className={`flex-1 text-center p-3 rounded-lg transition-all ${
                  taskSteps.find(s => s.id === 4)?.status === 'in_progress' 
                    ? 'bg-purple-100 ring-2 ring-purple-400 scale-105' 
                    : taskSteps.find(s => s.id === 4)?.status === 'completed'
                    ? 'bg-purple-50'
                    : 'bg-white/50'
                }`}>
                  <div className="text-2xl mb-1">⚖️</div>
                  <div className="text-xs font-bold text-gray-900">Judge</div>
                  {taskSteps.find(s => s.id === 4)?.status === 'completed' && (
                    <CheckCircle className="w-4 h-4 text-green-600 mx-auto mt-1" />
                  )}
                </div>
              </div>
            </div>
          )}

          {/* Task Steps */}
          <div className="flex-1 overflow-y-auto p-6">
            {taskSteps.length > 0 ? (
              <div className="space-y-4">
                {taskSteps.map((step, index) => (
                  <div
                    key={step.id}
                    className={`card slide-in stagger-${Math.min(index + 1, 5)}`}
                    style={{ animationFillMode: 'both' }}
                  >
                    <div className="flex items-start space-x-4">
                      <div className={`w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0 ${
                        step.status === 'completed'
                          ? 'bg-gradient-to-br from-green-500 to-emerald-600'
                          : step.status === 'in_progress'
                          ? 'bg-gradient-to-br from-blue-500 to-blue-600 animate-pulse'
                          : 'bg-gray-200'
                      }`}>
                        {step.status === 'completed' ? (
                          <CheckCircle className="w-5 h-5 text-white" />
                        ) : step.status === 'in_progress' ? (
                          <Loader className="w-5 h-5 text-white animate-spin" />
                        ) : (
                          <Clock className="w-5 h-5 text-gray-400" />
                        )}
                      </div>
                      <div className="flex-1">
                        <h3 className={`font-bold ${
                          step.status === 'completed' ? 'text-green-700' :
                          step.status === 'in_progress' ? 'text-blue-700' :
                          'text-gray-500'
                        }`}>
                          {step.title}
                        </h3>
                        {step.details && (
                          <p className="text-sm text-gray-600 mt-1">{step.details}</p>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="flex items-center justify-center h-full">
                <div className="text-center">
                  <div className="w-20 h-20 bg-gradient-to-br from-primary-100 to-purple-100 rounded-2xl flex items-center justify-center mx-auto mb-4 float">
                    <Activity className="w-10 h-10 text-primary-600" />
                  </div>
                  <h3 className="text-xl font-bold text-gray-900 mb-2">Ready to Analyze</h3>
                  <p className="text-gray-600 max-w-sm mx-auto">
                    Ask the AI assistant to analyze events, and I'll show you the real-time execution here.
                  </p>
                </div>
              </div>
            )}

            {/* Analysis Results */}
            {analysis && !analyzing && (
              <div className="mt-6 slide-in">
                <div className="card">
                  <h3 className="text-xl font-bold text-gray-900 mb-4">Analysis Results</h3>
                  <div className="space-y-4">
                    <div className="bg-gradient-to-br from-primary-50 to-purple-50 rounded-xl p-4 border-2 border-primary-200">
                      <div className="flex items-center justify-between mb-2">
                        <span className="font-bold text-gray-900">Winner</span>
                        <span className="text-2xl font-black text-primary-600">
                          {analysis.judge_decision.winner}
                        </span>
                      </div>
                      <p className="text-sm text-gray-700">{analysis.judge_decision.reasoning}</p>
                    </div>
                    
                    <div className="grid grid-cols-2 gap-4">
                      <div className="bg-white rounded-xl p-4 border-2 border-safety-200">
                        <div className="text-sm text-gray-600 mb-1">SafetyLab Score</div>
                        <div className="text-3xl font-black text-safety-600">
                          {(analysis.judge_decision.safety_lab_score * 100).toFixed(0)}%
                        </div>
                      </div>
                      <div className="bg-white rounded-xl p-4 border-2 border-performance-200">
                        <div className="text-sm text-gray-600 mb-1">PerformanceLab Score</div>
                        <div className="text-3xl font-black text-performance-600">
                          {(analysis.judge_decision.performance_lab_score * 100).toFixed(0)}%
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
