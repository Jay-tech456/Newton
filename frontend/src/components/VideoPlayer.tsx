import { useState, useEffect, useRef } from 'react'
import { Play, Pause, SkipBack, SkipForward, Maximize2, Volume2, VolumeX } from 'lucide-react'

interface VideoPlayerProps {
  datasetId: number
  frameCount: number
  duration: number
  startFrame?: number
  endFrame?: number
  autoPlay?: boolean
}

export default function VideoPlayer({
  datasetId,
  frameCount,
  duration,
  startFrame = 1,
  endFrame,
  autoPlay = false
}: VideoPlayerProps) {
  const [currentFrame, setCurrentFrame] = useState(startFrame)
  const [isPlaying, setIsPlaying] = useState(autoPlay)
  const [playbackSpeed, setPlaybackSpeed] = useState(1)
  const [isMuted, setIsMuted] = useState(true)
  const intervalRef = useRef<NodeJS.Timeout | null>(null)
  const containerRef = useRef<HTMLDivElement>(null)

  const maxFrame = endFrame || frameCount
  const fps = frameCount / duration
  const frameInterval = (1000 / fps) / playbackSpeed

  useEffect(() => {
    if (isPlaying) {
      intervalRef.current = setInterval(() => {
        setCurrentFrame(prev => {
          if (prev >= maxFrame) {
            setIsPlaying(false)
            return startFrame
          }
          return prev + 1
        })
      }, frameInterval)
    } else {
      if (intervalRef.current) {
        clearInterval(intervalRef.current)
      }
    }

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current)
      }
    }
  }, [isPlaying, frameInterval, maxFrame, startFrame])

  const togglePlay = () => {
    setIsPlaying(!isPlaying)
  }

  const handleSeek = (e: React.ChangeEvent<HTMLInputElement>) => {
    const frame = parseInt(e.target.value)
    setCurrentFrame(frame)
  }

  const skipBackward = () => {
    setCurrentFrame(Math.max(startFrame, currentFrame - Math.floor(fps)))
  }

  const skipForward = () => {
    setCurrentFrame(Math.min(maxFrame, currentFrame + Math.floor(fps)))
  }

  const toggleFullscreen = () => {
    if (!document.fullscreenElement && containerRef.current) {
      containerRef.current.requestFullscreen()
    } else if (document.fullscreenElement) {
      document.exitFullscreen()
    }
  }

  const getCurrentTime = () => {
    return ((currentFrame - 1) / fps).toFixed(2)
  }

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60)
    const secs = Math.floor(seconds % 60)
    return `${mins}:${secs.toString().padStart(2, '0')}`
  }

  // Frame URL - adjust based on your API structure
  const frameUrl = `/api/datasets/${datasetId}/frames/${currentFrame}`

  return (
    <div 
      ref={containerRef}
      className="bg-black rounded-lg overflow-hidden shadow-lg"
    >
      {/* Video Display */}
      <div className="relative aspect-video bg-gray-900">
        <img
          src={frameUrl}
          alt={`Frame ${currentFrame}`}
          className="w-full h-full object-contain"
          onError={(e) => {
            // Fallback placeholder
            e.currentTarget.src = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600"%3E%3Crect fill="%23333" width="800" height="600"/%3E%3Ctext x="50%25" y="50%25" fill="%23666" text-anchor="middle" dy=".3em" font-family="Arial" font-size="24"%3EFrame ' + currentFrame + '%3C/text%3E%3C/svg%3E'
          }}
        />

        {/* Frame Info Overlay */}
        <div className="absolute top-4 left-4 bg-black bg-opacity-70 px-3 py-2 rounded text-white text-sm font-mono">
          <div>Frame: {currentFrame} / {maxFrame}</div>
          <div>Time: {formatTime(parseFloat(getCurrentTime()))}</div>
        </div>

        {/* Playback Speed Indicator */}
        {playbackSpeed !== 1 && (
          <div className="absolute top-4 right-4 bg-black bg-opacity-70 px-3 py-2 rounded text-white text-sm font-mono">
            {playbackSpeed}x
          </div>
        )}

        {/* Center Play Button Overlay */}
        {!isPlaying && (
          <button
            onClick={togglePlay}
            className="absolute inset-0 flex items-center justify-center group"
          >
            <div className="w-20 h-20 bg-white bg-opacity-90 rounded-full flex items-center justify-center group-hover:bg-opacity-100 transition-all">
              <Play className="w-10 h-10 text-gray-900 ml-1" />
            </div>
          </button>
        )}
      </div>

      {/* Controls */}
      <div className="bg-gray-900 px-4 py-3 space-y-3">
        {/* Progress Bar */}
        <div className="flex items-center space-x-3">
          <span className="text-white text-xs font-mono min-w-[45px]">
            {formatTime(parseFloat(getCurrentTime()))}
          </span>
          <input
            type="range"
            min={startFrame}
            max={maxFrame}
            value={currentFrame}
            onChange={handleSeek}
            className="flex-1 h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer slider"
            style={{
              background: `linear-gradient(to right, #3b82f6 0%, #3b82f6 ${((currentFrame - startFrame) / (maxFrame - startFrame)) * 100}%, #374151 ${((currentFrame - startFrame) / (maxFrame - startFrame)) * 100}%, #374151 100%)`
            }}
          />
          <span className="text-white text-xs font-mono min-w-[45px]">
            {formatTime(duration)}
          </span>
        </div>

        {/* Control Buttons */}
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            {/* Play/Pause */}
            <button
              onClick={togglePlay}
              className="p-2 hover:bg-gray-800 rounded-lg transition-colors"
            >
              {isPlaying ? (
                <Pause className="w-5 h-5 text-white" />
              ) : (
                <Play className="w-5 h-5 text-white" />
              )}
            </button>

            {/* Skip Backward */}
            <button
              onClick={skipBackward}
              className="p-2 hover:bg-gray-800 rounded-lg transition-colors"
            >
              <SkipBack className="w-5 h-5 text-white" />
            </button>

            {/* Skip Forward */}
            <button
              onClick={skipForward}
              className="p-2 hover:bg-gray-800 rounded-lg transition-colors"
            >
              <SkipForward className="w-5 h-5 text-white" />
            </button>

            {/* Volume */}
            <button
              onClick={() => setIsMuted(!isMuted)}
              className="p-2 hover:bg-gray-800 rounded-lg transition-colors"
            >
              {isMuted ? (
                <VolumeX className="w-5 h-5 text-white" />
              ) : (
                <Volume2 className="w-5 h-5 text-white" />
              )}
            </button>
          </div>

          <div className="flex items-center space-x-2">
            {/* Playback Speed */}
            <select
              value={playbackSpeed}
              onChange={(e) => setPlaybackSpeed(parseFloat(e.target.value))}
              className="bg-gray-800 text-white text-sm px-3 py-1 rounded hover:bg-gray-700 transition-colors"
            >
              <option value="0.25">0.25x</option>
              <option value="0.5">0.5x</option>
              <option value="1">1x</option>
              <option value="1.5">1.5x</option>
              <option value="2">2x</option>
            </select>

            {/* Fullscreen */}
            <button
              onClick={toggleFullscreen}
              className="p-2 hover:bg-gray-800 rounded-lg transition-colors"
            >
              <Maximize2 className="w-5 h-5 text-white" />
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
