import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import App from './App'
import Home from './pages/Home'
import StoryGenerator from './pages/StoryGenerator'
import EpisodeScripts from './pages/EpisodeScripts'
import ThumbnailSelect from './pages/ThumbnailSelect'
import AudioGenerator from './pages/AudioGenerator'
// import FinalSummary from './pages/FinalSummary'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/story" element={<StoryGenerator />} />
        <Route path="/scripts" element={<EpisodeScripts />} />
        <Route path="/thumbnail" element={<ThumbnailSelect />} />
        <Route path="/audio" element={<AudioGenerator />} />
        {/* <Route path="/summary" element={<FinalSummary />} /> */}
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
)
