import { useState, useEffect, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import { Send, Bot, User, Sparkles, Database, Zap, TrendingUp, ArrowRight, BookOpen } from 'lucide-react'
import { api } from '../api/client'
import type { Dataset } from '../types'
import ScenarioGuide from '../components/ScenarioGuide'

interface Message {
  id: number
  role: 'user' | 'assistant' | 'system'
  content: string
  timestamp: Date
  action?: {
    type: 'navigate' | 'show_datasets'
    data?: any
  }
}

export default function HomePage() {
  const navigate = useNavigate()
  const [activeTab, setActiveTab] = useState<'chat' | 'scenarios'>('chat')
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 1,
      role: 'assistant',
      content: 'Welcome to AutoLab Drive! 🚗✨\n\nI\'m your AI assistant for autonomous driving research. I can help you:\n\n• Upload and analyze driving datasets\n• Run multi-agent research analysis\n• Compare safety vs performance strategies\n• Generate insights and recommendations\n\nWhat would you like to do today?',
      timestamp: new Date()
    }
  ])
  const [inputMessage, setInputMessage] = useState('')
  const [isTyping, setIsTyping] = useState(false)
  const [datasets, setDatasets] = useState<Dataset[]>([])
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    loadDatasets()
  }, [])

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const loadDatasets = async () => {
    try {
      const data = await api.getDatasets()
      setDatasets(data)
    } catch (error) {
      console.error('Failed to load datasets:', error)
    }
  }

  const addAssistantMessage = (content: string, action?: Message['action']) => {
    setMessages(prev => [...prev, {
      id: Date.now(),
      role: 'assistant',
      content,
      timestamp: new Date(),
      action
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

    // Simulate AI response
    setTimeout(() => {
      handleUserQuery(userMessage.content)
      setIsTyping(false)
    }, 1000)
  }

  const handleUserQuery = (query: string) => {
    const lowerQuery = query.toLowerCase()

    if (lowerQuery.includes('upload') || lowerQuery.includes('new dataset') || lowerQuery.includes('add dataset')) {
      addAssistantMessage(
        'Great! To upload a new dataset, click the "Upload Dataset" button below or navigate to the Datasets page. You can upload ZIP files containing driving frames and telemetry data.',
        { type: 'navigate', data: '/datasets' }
      )
    } else if (lowerQuery.includes('dataset') || lowerQuery.includes('show') || lowerQuery.includes('list')) {
      if (datasets.length > 0) {
        const datasetList = datasets.map((d, i) => `${i + 1}. ${d.name} (${d.frame_count.toLocaleString()} frames, ${d.duration_seconds}s)`).join('\n')
        addAssistantMessage(
          `I found ${datasets.length} dataset${datasets.length > 1 ? 's' : ''} in your workspace:\n\n${datasetList}\n\nClick on any dataset below to analyze it!`,
          { type: 'show_datasets' }
        )
      } else {
        addAssistantMessage(
          'You don\'t have any datasets yet. Would you like to upload one? I can guide you through the process!'
        )
      }
    } else if (lowerQuery.includes('analyze') || lowerQuery.includes('analysis')) {
      if (datasets.length > 0) {
        addAssistantMessage(
          `You have ${datasets.length} dataset${datasets.length > 1 ? 's' : ''} ready for analysis. Select a dataset below to start the multi-agent research process!`,
          { type: 'show_datasets' }
        )
      } else {
        addAssistantMessage(
          'To run analysis, you first need to upload a dataset. Would you like me to show you how?'
        )
      }
    } else if (lowerQuery.includes('help') || lowerQuery.includes('what can you do')) {
      addAssistantMessage(
        `I'm your autonomous driving research assistant! Here's what I can help with:\n\n🚗 **Dataset Management**\n• Upload driving datasets (ZIP format)\n• View and organize your data\n\n🔬 **Multi-Agent Analysis**\n• SafetyLab: Focuses on collision avoidance\n• PerformanceLab: Optimizes efficiency\n• Judge: Evaluates and compares strategies\n\n📊 **Insights & Evolution**\n• Generate research insights\n• Track strategy improvements\n• Compare performance metrics\n\nTry asking: "Show my datasets" or "Upload a new dataset"`
      )
    } else if (lowerQuery.includes('how') || lowerQuery.includes('work') || lowerQuery.includes('explain')) {
      addAssistantMessage(
        `AutoLab Drive uses a **self-evolving multi-agent system**:\n\n1️⃣ **Upload**: You provide driving datasets with events\n\n2️⃣ **Analyze**: Two AI labs compete:\n   • SafetyLab prioritizes collision avoidance\n   • PerformanceLab optimizes efficiency\n\n3️⃣ **Judge**: An impartial AI evaluates both approaches\n\n4️⃣ **Evolve**: Winning strategies improve the system\n\nThe system learns from each analysis, becoming smarter over time! 🧠✨`
      )
    } else {
      addAssistantMessage(
        `I understand you're asking about: "${query}"\n\nI can help you with:\n• Managing datasets\n• Running analysis\n• Understanding results\n\nTry asking "show my datasets" or "help" for more options!`
      )
    }
  }

  const handleDatasetClick = (datasetId: number) => {
    navigate(`/datasets/${datasetId}/analyze`)
  }

  return (
    <div className="min-h-screen flex flex-col pb-24">
      {/* Hero Section with Background Image */}
      <div className="hero-bg relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-b from-black/30 via-transparent to-black/50"></div>
        
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="text-center mb-8 fade-scale-in">
            <div className="flex items-center justify-center space-x-3 mb-4">
              <div className="w-16 h-16 gradient-bg rounded-2xl flex items-center justify-center shadow-2xl float">
                <Sparkles className="w-8 h-8 text-white" />
              </div>
            </div>
            <h1 className="text-6xl font-black text-white mb-4 drop-shadow-2xl tracking-tight">
              AUTOLAB DRIVE
            </h1>
            <p className="text-2xl text-white/90 max-w-2xl mx-auto font-light tracking-wide drop-shadow-lg">
              Self-Evolving Multi-Agent Research System
            </p>
            <p className="text-lg text-white/70 mt-2 font-light">
              for Autonomous Driving
            </p>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <div className="card text-center slide-in stagger-1" style={{ animationFillMode: 'both' }}>
              <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl flex items-center justify-center mx-auto mb-3 shadow-lg">
                <Database className="w-6 h-6 text-white" />
              </div>
              <div className="text-3xl font-black text-gray-900 mb-1">{datasets.length}</div>
              <div className="text-sm text-gray-600">Active Datasets</div>
            </div>
            <div className="card text-center slide-in stagger-2" style={{ animationFillMode: 'both' }}>
              <div className="w-12 h-12 bg-gradient-to-br from-green-500 to-emerald-600 rounded-xl flex items-center justify-center mx-auto mb-3 shadow-lg">
                <Zap className="w-6 h-6 text-white" />
              </div>
              <div className="text-3xl font-black text-gray-900 mb-1">2</div>
              <div className="text-sm text-gray-600">AI Research Labs</div>
            </div>
            <div className="card text-center slide-in stagger-3" style={{ animationFillMode: 'both' }}>
              <div className="w-12 h-12 bg-gradient-to-br from-purple-500 to-pink-600 rounded-xl flex items-center justify-center mx-auto mb-3 shadow-lg">
                <TrendingUp className="w-6 h-6 text-white" />
              </div>
              <div className="text-3xl font-black text-gray-900 mb-1">∞</div>
              <div className="text-sm text-gray-600">Self-Evolving</div>
            </div>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex space-x-2 border-b border-gray-200">
          <button
            onClick={() => setActiveTab('chat')}
            className={`px-6 py-3 font-medium transition-all ${
              activeTab === 'chat'
                ? 'text-primary-600 border-b-2 border-primary-600'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            <div className="flex items-center space-x-2">
              <Bot className="w-5 h-5" />
              <span>AI Assistant</span>
            </div>
          </button>
          <button
            onClick={() => setActiveTab('scenarios')}
            className={`px-6 py-3 font-medium transition-all ${
              activeTab === 'scenarios'
                ? 'text-primary-600 border-b-2 border-primary-600'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            <div className="flex items-center space-x-2">
              <BookOpen className="w-5 h-5" />
              <span>Scenario Guide</span>
            </div>
          </button>
        </div>
      </div>

      {/* Tab Content */}
      <div className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 pb-24">
        {activeTab === 'chat' ? (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 min-h-[600px]">
            {/* Chat Panel */}
            <div className="lg:col-span-2 card flex flex-col h-full">
              {/* Chat Header */}
              <div className="border-b border-gray-200 pb-4 mb-4">
                <div className="flex items-center space-x-3">
                  <div className="w-12 h-12 gradient-bg rounded-xl flex items-center justify-center shadow-lg">
                    <Bot className="w-6 h-6 text-white" />
                  </div>
                  <div>
                    <h2 className="text-xl font-bold text-gray-900">AI Assistant</h2>
                    <p className="text-sm text-gray-600">Ask me anything about autonomous driving research</p>
                  </div>
                </div>
              </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto space-y-4 mb-4">
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'} slide-in`}
                >
                  <div className={`flex items-start space-x-3 max-w-[85%] ${message.role === 'user' ? 'flex-row-reverse space-x-reverse' : ''}`}>
                    <div className={`w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0 shadow-md ${
                      message.role === 'user' 
                        ? 'bg-gradient-to-br from-primary-500 to-purple-600' 
                        : 'bg-gradient-to-br from-green-500 to-emerald-600'
                    }`}>
                      {message.role === 'user' ? (
                        <User className="w-5 h-5 text-white" />
                      ) : (
                        <Bot className="w-5 h-5 text-white" />
                      )}
                    </div>
                    <div className={`rounded-2xl px-5 py-3 ${
                      message.role === 'user'
                        ? 'bg-gradient-to-br from-primary-500 to-purple-600 text-white'
                        : 'bg-white border-2 border-gray-200 text-gray-900'
                    }`}>
                      <p className="text-sm whitespace-pre-wrap leading-relaxed">{message.content}</p>
                      {message.action?.type === 'navigate' && (
                        <button
                          onClick={() => navigate(message.action!.data)}
                          className="mt-3 inline-flex items-center space-x-2 bg-white text-primary-600 px-4 py-2 rounded-lg font-medium hover:bg-gray-50 transition-all hover:scale-105"
                        >
                          <span>Go to Datasets</span>
                          <ArrowRight className="w-4 h-4" />
                        </button>
                      )}
                      {message.action?.type === 'show_datasets' && datasets.length > 0 && (
                        <div className="mt-3 space-y-2">
                          {datasets.slice(0, 3).map(dataset => (
                            <button
                              key={dataset.id}
                              onClick={() => handleDatasetClick(dataset.id)}
                              className="w-full bg-white text-left px-4 py-3 rounded-lg border-2 border-gray-200 hover:border-primary-400 transition-all hover:scale-105 group"
                            >
                              <div className="flex items-center justify-between">
                                <div>
                                  <div className="font-bold text-gray-900 group-hover:text-primary-600 transition-colors">
                                    {dataset.name}
                                  </div>
                                  <div className="text-xs text-gray-500">
                                    {dataset.frame_count.toLocaleString()} frames • {dataset.duration_seconds}s
                                  </div>
                                </div>
                                <ArrowRight className="w-5 h-5 text-gray-400 group-hover:text-primary-600 transition-colors" />
                              </div>
                            </button>
                          ))}
                        </div>
                      )}
                      <p className={`text-xs mt-2 ${
                        message.role === 'user' ? 'text-white/70' : 'text-gray-500'
                      }`}>
                        {message.timestamp.toLocaleTimeString()}
                      </p>
                    </div>
                  </div>
                </div>
              ))}
              
              {isTyping && (
                <div className="flex justify-start slide-in">
                  <div className="flex items-start space-x-3">
                    <div className="w-10 h-10 rounded-xl flex items-center justify-center bg-gradient-to-br from-green-500 to-emerald-600 shadow-md">
                      <Bot className="w-5 h-5 text-white" />
                    </div>
                    <div className="bg-white border-2 border-gray-200 rounded-2xl px-5 py-3">
                      <div className="flex space-x-2">
                        <div className="w-2 h-2 bg-primary-500 rounded-full animate-bounce"></div>
                        <div className="w-2 h-2 bg-primary-500 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                        <div className="w-2 h-2 bg-primary-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                      </div>
                    </div>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>

            {/* Input */}
            <div className="border-t border-gray-200 pt-4">
              <div className="flex space-x-3">
                <input
                  type="text"
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                  placeholder="Ask me anything... (e.g., 'Show my datasets', 'How does this work?')"
                  className="flex-1 px-4 py-3 border-2 border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all bg-white"
                  disabled={isTyping}
                />
                <button
                  onClick={handleSendMessage}
                  disabled={!inputMessage.trim() || isTyping}
                  className="btn-primary px-6 py-3 flex items-center space-x-2"
                >
                  <Send className="w-5 h-5" />
                  <span>Send</span>
                </button>
              </div>
            </div>
          </div>

          {/* Quick Actions */}
          <div className="space-y-4">
            <div className="card">
              <h3 className="text-lg font-bold text-gray-900 mb-4">Quick Actions</h3>
              <div className="space-y-3">
                <button
                  onClick={() => navigate('/datasets')}
                  className="w-full btn-primary justify-center"
                >
                  <Database className="w-5 h-5 mr-2" />
                  View All Datasets
                </button>
                <button
                  onClick={() => setInputMessage('Show my datasets')}
                  className="w-full btn-secondary justify-center"
                >
                  <Zap className="w-5 h-5 mr-2" />
                  Start Analysis
                </button>
              </div>
            </div>

            <div className="card bg-gradient-to-br from-primary-50 to-purple-50 border-2 border-primary-200">
              <h3 className="text-lg font-bold text-gray-900 mb-2">💡 Try Asking</h3>
              <div className="space-y-2 text-sm">
                <button
                  onClick={() => setInputMessage('Show my datasets')}
                  className="w-full text-left px-3 py-2 bg-white rounded-lg hover:bg-gray-50 transition-colors text-gray-700"
                >
                  "Show my datasets"
                </button>
                <button
                  onClick={() => setInputMessage('How does this work?')}
                  className="w-full text-left px-3 py-2 bg-white rounded-lg hover:bg-gray-50 transition-colors text-gray-700"
                >
                  "How does this work?"
                </button>
                <button
                  onClick={() => setInputMessage('Upload a new dataset')}
                  className="w-full text-left px-3 py-2 bg-white rounded-lg hover:bg-gray-50 transition-colors text-gray-700"
                >
                  "Upload a new dataset"
                </button>
              </div>
            </div>
          </div>
        </div>
        ) : (
          <ScenarioGuide />
        )}
      </div>
    </div>
  )
}
