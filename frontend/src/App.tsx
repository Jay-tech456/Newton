import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import HomePage from './pages/HomePage'
import DatasetsPage from './pages/DatasetsPage'
import DatasetDetailPage from './pages/DatasetDetailPage'
import AnalysisWorkspace from './pages/AnalysisWorkspace'
import StrategiesPage from './pages/StrategiesPage'

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/datasets" element={<DatasetsPage />} />
          <Route path="/datasets/:datasetId" element={<DatasetDetailPage />} />
          <Route path="/datasets/:datasetId/analyze" element={<AnalysisWorkspace />} />
          <Route path="/strategies" element={<StrategiesPage />} />
        </Routes>
      </Layout>
    </Router>
  )
}

export default App
