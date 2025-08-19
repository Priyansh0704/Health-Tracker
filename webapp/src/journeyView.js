import './App.css';
import { useState } from 'react';
import episodes from './data/journey_episodes.json';
import allChats from './data/all_chats.json';

// The only change is the function name here
function JourneyView() { 
  // All your existing state and logic for displaying chats and episodes goes here...
  // ... (the rest of the code from your previous App.js)
  const [selectedEpisode, setSelectedEpisode] = useState(null);
  const [selectedChats, setSelectedChats] = useState([]);
  const [decisionTrace, setDecisionTrace] = useState(null);

  const handleEpisodeClick = (episode) => {
    setSelectedEpisode(episode);
    const dateParts = episode.date_range.split(' ');
    const startDate = new Date(`2025 ${dateParts[0]} ${dateParts[1]}`);
    if (isNaN(startDate)) {
        console.error("Invalid date format in episode:", episode.date_range);
        setSelectedChats([]);
        return;
    }
    const endDate = new Date(startDate);
    endDate.setDate(startDate.getDate() + 7);
    const filteredChats = allChats.filter(chat => {
      const chatDate = new Date(chat.ts.split(' ')[0]);
      return chatDate >= startDate && chatDate < endDate;
    });
    setSelectedChats(filteredChats);
  };
  
  const handleDecisionClick = (decisionId) => {
    import(`./data/decisions/${decisionId}.json`)
      .then(data => { setDecisionTrace(data.default); })
      .catch(err => { console.error("Could not load decision trace:", err); });
  };

  const closeModal = () => { setDecisionTrace(null); };

  return (
    <div className="app-container">
      {/* The entire JSX for the two-panel chat/episode view */}
      {/* Left Panel */}
      <div className="episode-list-panel">
        <div className="panel-header"><h2>Rohan's Journey</h2></div>
        <div className="episodes-list">
          {episodes.map((episode, index) => (
            <div key={index} className={`episode-card ${selectedEpisode === episode ? 'active' : ''}`} onClick={() => handleEpisodeClick(episode)}>
              <h4>{episode.title}</h4><p>{episode.date_range}</p>
            </div>
          ))}
        </div>
      </div>
      {/* Right Panel */}
      <div className="chat-window-panel">
        <div className="panel-header"><h3>{selectedEpisode ? selectedEpisode.title : 'Conversation Details'}</h3></div>
        <div className="chat-messages">
          {selectedChats.length > 0 ? (
            selectedChats.map(chat => {
              const isDecision = chat.text.includes('[DECISION:id=');
              const decisionId = isDecision ? chat.text.match(/\[DECISION:id=([^\]]+)\]/)[1] : null;
              return (<div key={chat.id} className={`chat-bubble ${chat.role === 'member' ? 'member' : 'team'} ${isDecision ? 'decision' : ''}`} onClick={() => isDecision && handleDecisionClick(decisionId)} title={isDecision ? 'Click to see rationale' : ''}>
                  <strong>{chat.sender}</strong><p>{chat.text}</p>
                </div>);
            })
          ) : (<p className="placeholder-text">Select an episode to see the conversation.</p>)}
        </div>
      </div>
      {/* Modal */}
      {decisionTrace && (
        <div className="modal-overlay" onClick={closeModal}>
          <div className="modal-content" onClick={e => e.stopPropagation()}>
            <h3>Decision Rationale</h3><h4 className="decision-id">{decisionTrace.decision_id}</h4>
            <p className="decision-summary">{decisionTrace.summary}</p>
            <div className="rationale-section"><strong>Trigger:</strong><p>{decisionTrace.trigger}</p></div>
            <div className="rationale-section"><strong>Rationale:</strong><ul>{decisionTrace.rationale.map((point, i) => <li key={i}>{point}</li>)}</ul></div>
            <p><strong>Decision Owner:</strong> {decisionTrace.owner}</p>
            <button className="close-button" onClick={closeModal}>Close</button>
          </div>
        </div>
      )}
    </div>
  );
}

// And change the export name
export default JourneyView;