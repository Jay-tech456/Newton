import { Event } from '../types'
import { useState } from 'react'

interface EventTimelineProps {
  events: Event[]
  selectedEvent: Event | null
  onEventSelect: (event: Event) => void
  duration: number
}

export default function EventTimeline({
  events,
  selectedEvent,
  onEventSelect,
  duration,
}: EventTimelineProps) {
  const [hoveredEvent, setHoveredEvent] = useState<Event | null>(null)

  const getEventColor = (eventType: string) => {
    switch (eventType) {
      case 'cut_in':
        return 'bg-gradient-to-r from-red-500 to-red-600'
      case 'pedestrian':
        return 'bg-gradient-to-r from-orange-500 to-orange-600'
      case 'adverse_weather':
        return 'bg-gradient-to-r from-blue-500 to-blue-600'
      case 'close_following':
        return 'bg-gradient-to-r from-yellow-500 to-yellow-600'
      case 'sudden_brake':
        return 'bg-gradient-to-r from-purple-500 to-purple-600'
      case 'lane_change':
        return 'bg-gradient-to-r from-green-500 to-green-600'
      default:
        return 'bg-gradient-to-r from-gray-500 to-gray-600'
    }
  }

  const getEventDotColor = (eventType: string) => {
    switch (eventType) {
      case 'cut_in':
        return 'bg-red-500'
      case 'pedestrian':
        return 'bg-orange-500'
      case 'adverse_weather':
        return 'bg-blue-500'
      case 'close_following':
        return 'bg-yellow-500'
      case 'sudden_brake':
        return 'bg-purple-500'
      case 'lane_change':
        return 'bg-green-500'
      default:
        return 'bg-gray-500'
    }
  }

  const getEventPosition = (timestamp: number) => {
    return (timestamp / duration) * 100
  }

  return (
    <div className="space-y-6">
      {/* Timeline Bar */}
      <div className="relative">
        <div className="relative h-20 bg-gradient-to-r from-gray-100 via-gray-50 to-gray-100 rounded-xl overflow-hidden border-2 border-gray-200 shadow-inner">
          {/* Time markers */}
          <div className="absolute inset-0 flex items-end px-3 pb-2">
            {[0, 25, 50, 75, 100].map((percent) => (
              <div
                key={percent}
                className="absolute text-xs font-semibold text-gray-600"
                style={{ left: `${percent}%`, transform: 'translateX(-50%)' }}
              >
                {((duration * percent) / 100).toFixed(0)}s
              </div>
            ))}
          </div>

          {/* Progress line */}
          <div className="absolute top-3 left-0 right-0 h-0.5 bg-gray-300"></div>

          {/* Event markers */}
          {events.map((event) => {
            const position = getEventPosition(event.start_timestamp)
            const width = ((event.end_timestamp - event.start_timestamp) / duration) * 100
            const isSelected = selectedEvent?.id === event.id
            const isHovered = hoveredEvent?.id === event.id

            return (
              <div
                key={event.id}
                className={`absolute top-2 h-10 cursor-pointer transition-all duration-300 ${
                  isSelected 
                    ? 'ring-4 ring-primary-400 ring-offset-2 z-20 scale-110' 
                    : isHovered
                    ? 'ring-2 ring-white ring-offset-2 z-10 scale-105'
                    : 'hover:scale-105 z-0'
                } ${getEventColor(event.event_type)} rounded-lg shadow-lg`}
                style={{
                  left: `${position}%`,
                  width: `${Math.max(width, 1.5)}%`,
                }}
                onClick={() => onEventSelect(event)}
                onMouseEnter={() => setHoveredEvent(event)}
                onMouseLeave={() => setHoveredEvent(null)}
              >
                {/* Pulse animation for selected */}
                {isSelected && (
                  <div className="absolute inset-0 rounded-lg animate-ping opacity-75 bg-primary-400"></div>
                )}
              </div>
            )
          })}

          {/* Tooltip for hovered event */}
          {hoveredEvent && (
            <div
              className="absolute top-14 bg-gray-900 text-white px-3 py-2 rounded-lg text-xs font-medium shadow-xl z-30 whitespace-nowrap pointer-events-none"
              style={{
                left: `${getEventPosition(hoveredEvent.start_timestamp)}%`,
                transform: 'translateX(-50%)',
              }}
            >
              <div className="font-bold">{hoveredEvent.event_type.replace(/_/g, ' ').toUpperCase()}</div>
              <div className="text-gray-300">{hoveredEvent.start_timestamp.toFixed(1)}s - {hoveredEvent.end_timestamp.toFixed(1)}s</div>
              <div className="absolute -top-1 left-1/2 transform -translate-x-1/2 w-2 h-2 bg-gray-900 rotate-45"></div>
            </div>
          )}
        </div>
      </div>

      {/* Event List */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
        {events.map((event, index) => (
          <button
            key={event.id}
            onClick={() => onEventSelect(event)}
            onMouseEnter={() => setHoveredEvent(event)}
            onMouseLeave={() => setHoveredEvent(null)}
            className={`px-4 py-3 rounded-xl text-left text-sm transition-all duration-300 slide-in stagger-${Math.min(index % 4 + 1, 5)} ${
              selectedEvent?.id === event.id
                ? 'bg-gradient-to-br from-primary-100 to-purple-100 border-2 border-primary-500 text-primary-900 shadow-lg scale-105'
                : 'bg-white/80 border-2 border-gray-200 text-gray-700 hover:bg-white hover:border-primary-300 hover:scale-105 hover:shadow-md'
            }`}
            style={{ animationFillMode: 'both' }}
          >
            <div className="flex items-center space-x-2 mb-1">
              <div className={`w-3 h-3 rounded-full ${getEventDotColor(event.event_type)} ${selectedEvent?.id === event.id ? 'animate-pulse' : ''}`} />
              <span className="font-bold truncate text-xs">
                {event.event_type.replace(/_/g, ' ').toUpperCase()}
              </span>
            </div>
            <div className="text-xs text-gray-600 font-medium">
              {event.start_timestamp.toFixed(1)}s
            </div>
          </button>
        ))}
      </div>
    </div>
  )
}
