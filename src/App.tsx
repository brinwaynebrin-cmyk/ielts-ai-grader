import { Routes, Route } from 'react-router'
import Home from './pages/Home'
import TypingPage from './pages/TypingPage'
import GrammarPage from './pages/GrammarPage'
import VocabularyPage from './pages/VocabularyPage'
import CollocationPage from './pages/CollocationPage'
import ListeningPage from './pages/ListeningPage'
import GamesPage from './pages/GamesPage'
import Layout from './components/Layout'

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<Home />} />
        <Route path="/typing" element={<TypingPage />} />
        <Route path="/grammar" element={<GrammarPage />} />
        <Route path="/vocabulary" element={<VocabularyPage />} />
        <Route path="/collocation" element={<CollocationPage />} />
        <Route path="/listening" element={<ListeningPage />} />
        <Route path="/games" element={<GamesPage />} />
      </Route>
    </Routes>
  )
}
