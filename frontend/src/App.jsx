import { Routes, Route, Link } from 'react-router-dom'

function App() {
  return (
    <div>
      <nav>
        <Link to="/socios">Socios</Link> |{' '}
        <Link to="/jugadores">Jugadores</Link> |{' '}
        <Link to="/partidos">Partidos</Link>
      </nav>
      <Routes>
        <Route path="/socios/*" element={<div>Socios</div>} />
        <Route path="/jugadores/*" element={<div>Jugadores</div>} />
        <Route path="/partidos/*" element={<div>Partidos</div>} />
      </Routes>
    </div>
  )
}

export default App
