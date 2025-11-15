import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { Upload, Plus, Calendar, Film, Clock, Zap, TrendingUp, Activity, Trash2 } from 'lucide-react'
import { api } from '../api/client'
import type { Dataset } from '../types'

export default function DatasetsPage() {
  const [datasets, setDatasets] = useState<Dataset[]>([])
  const [loading, setLoading] = useState(true)
  const [showUploadModal, setShowUploadModal] = useState(false)
  const [deleteConfirm, setDeleteConfirm] = useState<number | null>(null)
  const [deleting, setDeleting] = useState(false)

  useEffect(() => {
    loadDatasets()
  }, [])

  const loadDatasets = async () => {
    try {
      const data = await api.getDatasets()
      setDatasets(data)
    } catch (error) {
      console.error('Failed to load datasets:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (datasetId: number) => {
    setDeleting(true)
    try {
      await api.deleteDataset(datasetId)
      setDatasets(datasets.filter(d => d.id !== datasetId))
      setDeleteConfirm(null)
    } catch (error) {
      console.error('Failed to delete dataset:', error)
      alert('Failed to delete dataset. Please try again.')
    } finally {
      setDeleting(false)
    }
  }

  const formatDuration = (seconds: number) => {
    const minutes = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${minutes}:${secs.toString().padStart(2, '0')}`
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    })
  }

  return (
    <div className="space-y-8">
      {/* Hero Header */}
      <div className="fade-scale-in">
        <div className="glass rounded-2xl p-8 border-2 border-white/30">
          <div className="flex justify-between items-start">
            <div className="flex-1">
              <div className="flex items-center space-x-3 mb-3">
                <div className="w-12 h-12 gradient-bg rounded-xl flex items-center justify-center shadow-lg">
                  <Activity className="w-6 h-6 text-white" />
                </div>
                <h1 className="text-4xl font-bold bg-gradient-to-r from-gray-900 via-primary-600 to-purple-600 bg-clip-text text-transparent">
                  Datasets
                </h1>
              </div>
              <p className="text-gray-700 text-lg max-w-2xl">
                Upload and analyze driving datasets with multi-agent research labs powered by AI
              </p>
              <div className="flex items-center space-x-6 mt-4 text-sm">
                <div className="flex items-center space-x-2 text-primary-600">
                  <TrendingUp className="w-4 h-4" />
                  <span className="font-medium">{datasets.length} Active Datasets</span>
                </div>
              </div>
            </div>
            <button
              onClick={() => setShowUploadModal(true)}
              className="btn-primary flex items-center space-x-2 text-lg px-6 py-3"
            >
              <Plus className="w-5 h-5" />
              <span>Upload Dataset</span>
            </button>
          </div>
        </div>
      </div>

      {/* Datasets Grid */}
      {loading ? (
        <div className="flex items-center justify-center h-64">
          <div className="relative">
            <div className="animate-spin rounded-full h-16 w-16 border-4 border-primary-200"></div>
            <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-primary-600 absolute top-0"></div>
          </div>
        </div>
      ) : datasets.length === 0 ? (
        <div className="card text-center py-16 slide-in">
          <div className="float">
            <Upload className="w-20 h-20 text-primary-400 mx-auto mb-4" />
          </div>
          <h3 className="text-2xl font-bold text-gray-900 mb-2">No datasets yet</h3>
          <p className="text-gray-600 mb-8 text-lg">
            Upload your first driving dataset to get started with multi-agent analysis
          </p>
          <button
            onClick={() => setShowUploadModal(true)}
            className="btn-primary inline-flex items-center space-x-2 text-lg px-6 py-3"
          >
            <Plus className="w-5 h-5" />
            <span>Upload Dataset</span>
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {datasets.map((dataset, index) => (
            <div 
              key={dataset.id} 
              className={`card group cursor-pointer relative overflow-hidden slide-in stagger-${Math.min(index + 1, 5)}`}
              style={{ animationFillMode: 'both' }}
            >
              {/* Gradient overlay on hover */}
              <div className="absolute inset-0 bg-gradient-to-br from-primary-500/0 to-purple-500/0 group-hover:from-primary-500/10 group-hover:to-purple-500/10 transition-all duration-500 pointer-events-none"></div>
              
              <div className="relative z-10">
                <div className="flex items-start justify-between mb-4">
                  <div className="flex-1">
                    <h3 className="text-xl font-bold text-gray-900 mb-2 group-hover:text-primary-600 transition-colors">
                      {dataset.name}
                    </h3>
                    {dataset.description && (
                      <p className="text-sm text-gray-600 line-clamp-2">
                        {dataset.description}
                      </p>
                    )}
                  </div>
                </div>

                <div className="space-y-3 mb-4">
                  <div className="flex items-center text-sm text-gray-700 bg-gray-50 rounded-lg p-2 group-hover:bg-primary-50 transition-colors">
                    <Film className="w-5 h-5 mr-3 text-primary-500" />
                    <span className="font-medium">{dataset.frame_count.toLocaleString()} frames</span>
                  </div>
                  <div className="flex items-center text-sm text-gray-700 bg-gray-50 rounded-lg p-2 group-hover:bg-primary-50 transition-colors">
                    <Clock className="w-5 h-5 mr-3 text-purple-500" />
                    <span className="font-medium">{formatDuration(dataset.duration_seconds)}</span>
                  </div>
                  <div className="flex items-center text-sm text-gray-700 bg-gray-50 rounded-lg p-2 group-hover:bg-primary-50 transition-colors">
                    <Calendar className="w-5 h-5 mr-3 text-pink-500" />
                    <span className="font-medium">{formatDate(dataset.created_at)}</span>
                  </div>
                </div>

                <div className="space-y-2">
                  <div className="flex space-x-2">
                    <Link
                      to={`/datasets/${dataset.id}`}
                      className="flex-1 text-center px-4 py-2.5 text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 rounded-lg transition-all duration-200 border border-gray-200 hover:border-primary-300 hover:scale-105"
                    >
                      View Details
                    </Link>
                    <Link
                      to={`/datasets/${dataset.id}/analyze`}
                      className="flex-1 text-center px-4 py-2.5 text-sm font-medium text-white bg-gradient-to-r from-primary-600 to-purple-600 hover:from-primary-700 hover:to-purple-700 rounded-lg transition-all duration-200 flex items-center justify-center space-x-1 shadow-md hover:shadow-lg hover:scale-105"
                    >
                      <Zap className="w-4 h-4" />
                      <span>Analyze</span>
                    </Link>
                  </div>
                  {deleteConfirm === dataset.id ? (
                    <div className="flex space-x-2">
                      <button
                        onClick={() => handleDelete(dataset.id)}
                        disabled={deleting}
                        className="flex-1 px-4 py-2 text-sm font-medium text-white bg-red-600 hover:bg-red-700 rounded-lg transition-all disabled:opacity-50"
                      >
                        {deleting ? 'Deleting...' : 'Confirm Delete'}
                      </button>
                      <button
                        onClick={() => setDeleteConfirm(null)}
                        disabled={deleting}
                        className="flex-1 px-4 py-2 text-sm font-medium text-gray-700 bg-gray-200 hover:bg-gray-300 rounded-lg transition-all disabled:opacity-50"
                      >
                        Cancel
                      </button>
                    </div>
                  ) : (
                    <button
                      onClick={(e) => {
                        e.preventDefault()
                        setDeleteConfirm(dataset.id)
                      }}
                      className="w-full px-4 py-2 text-sm font-medium text-red-600 bg-red-50 hover:bg-red-100 rounded-lg transition-all duration-200 flex items-center justify-center space-x-2 border border-red-200 hover:border-red-300"
                    >
                      <Trash2 className="w-4 h-4" />
                      <span>Delete Dataset</span>
                    </button>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Upload Modal */}
      {showUploadModal && (
        <UploadModal
          onClose={() => setShowUploadModal(false)}
          onSuccess={() => {
            setShowUploadModal(false)
            loadDatasets()
          }}
        />
      )}
    </div>
  )
}

interface UploadModalProps {
  onClose: () => void
  onSuccess: () => void
}

function UploadModal({ onClose, onSuccess }: UploadModalProps) {
  const [file, setFile] = useState<File | null>(null)
  const [name, setName] = useState('')
  const [description, setDescription] = useState('')
  const [uploading, setUploading] = useState(false)
  const [error, setError] = useState('')
  const [dragActive, setDragActive] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!file || !name) return

    setUploading(true)
    setError('')

    try {
      await api.uploadDataset(file, name, description)
      onSuccess()
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to upload dataset')
    } finally {
      setUploading(false)
    }
  }

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true)
    } else if (e.type === 'dragleave') {
      setDragActive(false)
    }
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0])
    }
  }

  return (
    <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 fade-scale-in">
      <div className="glass rounded-2xl shadow-2xl max-w-md w-full mx-4 border-2 border-white/30">
        <div className="p-8">
          <div className="flex items-center space-x-3 mb-6">
            <div className="w-10 h-10 gradient-bg rounded-lg flex items-center justify-center">
              <Upload className="w-5 h-5 text-white" />
            </div>
            <h2 className="text-2xl font-bold bg-gradient-to-r from-gray-900 to-primary-600 bg-clip-text text-transparent">
              Upload Dataset
            </h2>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Dataset Name *
              </label>
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="input"
                placeholder="e.g., Highway Drive 2024-01"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Description
              </label>
              <textarea
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                className="input"
                rows={3}
                placeholder="Optional description..."
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                ZIP File *
              </label>
              <div
                className={`relative border-2 border-dashed rounded-xl p-6 transition-all duration-300 ${
                  dragActive
                    ? 'border-primary-500 bg-primary-50'
                    : file
                    ? 'border-green-500 bg-green-50'
                    : 'border-gray-300 hover:border-primary-400 bg-white/50'
                }`}
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
              >
                <input
                  type="file"
                  accept=".zip"
                  onChange={(e) => setFile(e.target.files?.[0] || null)}
                  className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                  required
                />
                <div className="text-center">
                  <Upload className={`w-10 h-10 mx-auto mb-2 ${
                    file ? 'text-green-500' : 'text-gray-400'
                  }`} />
                  {file ? (
                    <p className="text-sm font-medium text-green-700">{file.name}</p>
                  ) : (
                    <>
                      <p className="text-sm text-gray-600 font-medium">Drop your ZIP file here or click to browse</p>
                      <p className="text-xs text-gray-500 mt-1">Must contain frames/ directory and telemetry.csv</p>
                    </>
                  )}
                </div>
              </div>
            </div>

            {error && (
              <div className="bg-red-50 border-2 border-red-200 text-red-700 px-4 py-3 rounded-xl slide-in">
                <p className="font-medium">{error}</p>
              </div>
            )}

            <div className="flex space-x-3 pt-6">
              <button
                type="button"
                onClick={onClose}
                className="btn-secondary flex-1"
                disabled={uploading}
              >
                Cancel
              </button>
              <button
                type="submit"
                className="btn-primary flex-1 relative overflow-hidden"
                disabled={uploading || !file || !name}
              >
                {uploading && (
                  <div className="absolute inset-0 shimmer"></div>
                )}
                <span className="relative z-10">{uploading ? 'Uploading...' : 'Upload'}</span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}
