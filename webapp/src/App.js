import './App.css';
import { Routes, Route, Link } from 'react-router-dom';
import JourneyView from './journeyView'; // Import your new component
import Dashboard from './Dashboard';   // Import your dashboard component

function App() {
  return (
    <div>
      {/* Navigation Header */}
      <nav className="main-nav">
        <Link to="/">Journey View</Link>
        <Link to="/dashboard">Dashboard</Link>
      </nav>

      {/* Route Definitions */}
      <Routes>
        <Route path="/" element={<JourneyView />} />
        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
    </div>
  );
}

export default App;