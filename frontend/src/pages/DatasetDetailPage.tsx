import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { ArrowLeft, Play, AlertTriangle, Cloud, Car, Users, Zap, Activity, Clock, Film } from 'lucide-react'
import { api } from '../api/client'
import type { Dataset, Event, Analysis } from '../types'
import EventTimeline from '../components/EventTimeline'
import AnalysisPanel from '../components/AnalysisPanel'

export default function DatasetDetailPage() {
  const { datasetId } = useParams<{ datasetId: string }>()
  const [dataset, setDataset] = useState<Dataset | null>(null)
  const [events, setEvents] = useState<Event[]>([])
  const [selectedEvent, setSelectedEvent] = useState<Event | null>(null)
  const [analysis, setAnalysis] = useState<Analysis | null>(null)
  const [loading, setLoading] = useState(true)
  const [analyzing, setAnalyzing] = useState(false)

  useEffect(() => {
    if (datasetId) {
      loadDatasetAndEvents(parseInt(datasetId))
    }
  }, [datasetId])

  const loadDatasetAndEvents = async (id: number) => {
    try {
      const [datasetData, eventsData] = await Promise.all([
        api.getDataset(id),
        api.getDatasetEvents(id),
      ])
      setDataset(datasetData)
      setEvents(eventsData)
      if (eventsData.length > 0) {
        setSelectedEvent(eventsData[0])
        loadAnalysis(id, eventsData[0].id)
      }
    } catch (error) {
      console.error('Failed to load dataset:', error)
    } finally {
      setLoading(false)
    }
  }

  const loadAnalysis = async (datasetId: number, eventId: number) => {
    try {
      const analysisData = await api.getEventAnalysis(datasetId, eventId)
      setAnalysis(analysisData)
    } catch (error) {
      // No analysis yet
      setAnalysis(null)
    }
  }

  const handleAnalyze = async () => {
    if (!dataset || !selectedEvent) return

    setAnalyzing(true)
    try {
      const analysisData = await api.analyzeEvent(dataset.id, selectedEvent.id)
      setAnalysis(analysisData)
    } catch (error) {
      console.error('Failed to analyze event:', error)
    } finally {
      setAnalyzing(false)
    }
  }

  const handleEventSelect = (event: Event) => {
    setSelectedEvent(event)
    if (dataset) {
      loadAnalysis(dataset.id, event.id)
    }
  }

  const getEventIcon = (eventType: string) => {
    switch (eventType) {
      case 'cut_in':
        return <Car className="w-5 h-5" />
      case 'pedestrian':
        return <Users className="w-5 h-5" />
      case 'adverse_weather':
        return <Cloud className="w-5 h-5" />
      case 'sudden_brake':
        return <Zap className="w-5 h-5" />
      default:
        return <AlertTriangle className="w-5 h-5" />
    }
  }

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'high':
        return 'bg-red-100 text-red-800 border-red-200'
      case 'medium':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200'
      case 'low':
        return 'bg-green-100 text-green-800 border-green-200'
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200'
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
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
    <div className="space-y-6">
      {/* Header */}
      <div className="fade-scale-in">
        <Link to="/" className="inline-flex items-center text-primary-600 hover:text-primary-700 mb-4 font-medium transition-all hover:scale-105">
          <ArrowLeft className="w-4 h-4 mr-2" />
          Back to Datasets
        </Link>
        <div className="glass rounded-2xl p-8 border-2 border-white/30">
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <div className="flex items-center space-x-3 mb-3">
                <div className="w-12 h-12 gradient-bg rounded-xl flex items-center justify-center shadow-lg">
                  <Activity className="w-6 h-6 text-white" />
                </div>
                <h1 className="text-4xl font-bold bg-gradient-to-r from-gray-900 via-primary-600 to-purple-600 bg-clip-text text-transparent">
                  {dataset.name}
                </h1>
              </div>
              {dataset.description && (
                <p className="text-gray-700 text-lg mb-4">{dataset.description}</p>
              )}
              <div className="flex items-center space-x-6 text-sm">
                <div className="flex items-center space-x-2 bg-white/60 px-4 py-2 rounded-lg">
                  <Film className="w-4 h-4 text-primary-600" />
                  <span className="font-medium text-gray-900">{dataset.frame_count.toLocaleString()} frames</span>
                </div>
                <div className="flex items-center space-x-2 bg-white/60 px-4 py-2 rounded-lg">
                  <Clock className="w-4 h-4 text-purple-600" />
                  <span className="font-medium text-gray-900">{Math.floor(dataset.duration_seconds / 60)}:{(dataset.duration_seconds % 60).toString().padStart(2, '0')} duration</span>
                </div>
                <div className="flex items-center space-x-2 bg-white/60 px-4 py-2 rounded-lg">
                  <AlertTriangle className="w-4 h-4 text-orange-600" />
                  <span className="font-medium text-gray-900">{events.length} events detected</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Event Timeline */}
      <div className="card slide-in stagger-1" style={{ animationFillMode: 'both' }}>
        <div className="flex items-center space-x-3 mb-6">
          <div className="w-10 h-10 bg-gradient-to-br from-orange-500 to-red-600 rounded-lg flex items-center justify-center">
            <Zap className="w-5 h-5 text-white" />
          </div>
          <h2 className="text-2xl font-bold text-gray-900">Event Timeline</h2>
        </div>
        <EventTimeline
          events={events}
          selectedEvent={selectedEvent}
          onEventSelect={handleEventSelect}
          duration={dataset.duration_seconds}
        />
      </div>

      {/* Selected Event Details */}
      {selectedEvent && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Event Info */}
          <div className="card slide-in stagger-2" style={{ animationFillMode: 'both' }}>
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-xl font-bold text-gray-900">Event Details</h3>
              <div className={`px-4 py-2 rounded-full text-sm font-bold border-2 ${getSeverityColor(selectedEvent.severity)} shadow-md`}>
                {selectedEvent.severity.toUpperCase()}
              </div>
            </div>

            <div className="space-y-4">
              <div className="bg-gradient-to-br from-primary-50 to-purple-50 rounded-xl p-4 border border-primary-200">
                <div className="flex items-center space-x-3 mb-2">
                  <div className="w-10 h-10 bg-gradient-to-br from-primary-500 to-purple-600 rounded-lg flex items-center justify-center shadow-md">
                    {getEventIcon(selectedEvent.event_type)}
                  </div>
                  <p className="text-lg font-bold text-gray-900">
                    {selectedEvent.event_type.replace(/_/g, ' ').toUpperCase()}
                  </p>
                </div>
                <p className="text-sm text-gray-700">{selectedEvent.description}</p>
              </div>

              <div className="space-y-3 text-sm">
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

            <button
              onClick={handleAnalyze}
              disabled={analyzing}
              className="btn-primary w-full mt-6 flex items-center justify-center space-x-2 text-lg py-3 relative overflow-hidden"
            >
              {analyzing && (
                <div className="absolute inset-0 shimmer"></div>
              )}
              <Play className="w-5 h-5 relative z-10" />
              <span className="relative z-10">{analyzing ? 'Analyzing...' : 'Run Analysis'}</span>
            </button>
          </div>

          {/* Analysis Results */}
          <div className="lg:col-span-2 slide-in stagger-3" style={{ animationFillMode: 'both' }}>
            <AnalysisPanel analysis={analysis} loading={analyzing} />
          </div>
        </div>
      )}
    </div>
  )
}
