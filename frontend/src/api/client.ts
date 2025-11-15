import axios from 'axios'
import type { Dataset, Event, Analysis, GenomeEvolution } from '../types'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const api = {
  // Datasets
  uploadDataset: async (file: File, name: string, description?: string): Promise<Dataset> => {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('name', name)
    if (description) {
      formData.append('description', description)
    }

    const response = await apiClient.post('/api/upload-dataset', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },

  getDatasets: async (): Promise<Dataset[]> => {
    const response = await apiClient.get('/api/datasets')
    return response.data
  },

  getDataset: async (datasetId: number): Promise<Dataset> => {
    const response = await apiClient.get(`/api/datasets/${datasetId}`)
    return response.data
  },

  deleteDataset: async (datasetId: number): Promise<void> => {
    await apiClient.delete(`/api/datasets/${datasetId}`)
  },

  // Events
  getDatasetEvents: async (datasetId: number): Promise<Event[]> => {
    const response = await apiClient.get(`/api/datasets/${datasetId}/events`)
    return response.data
  },

  // Analysis
  analyzeEvent: async (datasetId: number, eventId: number): Promise<Analysis> => {
    const response = await apiClient.post(
      `/api/datasets/${datasetId}/events/${eventId}/analyze`
    )
    return response.data
  },

  getEventAnalysis: async (datasetId: number, eventId: number): Promise<Analysis> => {
    const response = await apiClient.get(
      `/api/datasets/${datasetId}/events/${eventId}/analysis`
    )
    return response.data
  },

  // Strategies
  getLabStrategies: async (): Promise<GenomeEvolution[]> => {
    const response = await apiClient.get('/api/labs/strategies')
    return response.data
  },

  getLabStrategyEvolution: async (labName: string): Promise<GenomeEvolution> => {
    const response = await apiClient.get(`/api/labs/${labName}/strategies`)
    return response.data
  },
}

export default apiClient
