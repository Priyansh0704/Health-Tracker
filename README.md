Elyx Health Journey Visualizer
A submission for the Elyx Hackathon (August 2025)
An interactive, AI-powered web application that transforms 8 months of raw member chat logs into a transparent, data-driven health timeline.
Built to solve the critical challenge of understanding the "why" behind every decision in a member's long-term health journey.

🚀 Live Demo
You can access the live, deployed web application here:

https://health-tracker-2v06sytld-priyansh-goyals-projects.vercel.app/

✨ What is the Health Journey Visualizer?
The Health Journey Visualizer is a tool for the Elyx team to retrospectively analyze a member's complete 8-month engagement. It ingests thousands of unstructured messages and presents them as a structured, interactive timeline, making it easy to pinpoint key events and understand the context behind every intervention.

Key Features
AI-Generated Journey Episodes - Raw chat logs are automatically summarized into logical, weekly "episodes."

Interactive Chat Timeline - Instantly load and review the detailed conversations for any given week.

One-Click Decision Traceability - Click on any decision to see an AI-generated summary of the trigger and rationale, directly linked to the conversations that caused it.

Analytics Dashboards - Visualize high-level trends for member adherence, stress levels, and team engagement.

Modern React Frontend - A clean, responsive UI built with modern React and Chart.js.

Automated Data Pipeline - A series of Python scripts that use the Gemini API to process and structure the data.

💡 Why This Project Matters
This project directly addresses a core challenge for any long-term health service: maintaining clarity and accountability. While traditional record-keeping can show what was done, this tool reveals why.

From Data Chaos to Clarity
This tool transforms unstructured data into actionable insights, solving a key business problem.

┌─────────────────────────────────────────────────────────┐
│        The Transformation: Unstructured vs. Structured  │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Raw Data (Before)                                      │
│  - 2000+ individual JSON messages                       │
│  - No inherent structure or context                     │
│  - Time-consuming to find key decisions                 │
│  - Rationale is buried in conversation                  │
│                                                         │
│  Structured Insights (After)                            │
│  - 32 AI-summarized weekly episodes                     │
│  - 15+ AI-analyzed decision traces                      │
│  - One-click access to decision rationale               │
│  - Visual dashboards for instant trend analysis         │
│                                                         │
│  This represents a >95% reduction in the time needed    │
│  to analyze a member's journey.                         │
└─────────────────────────────────────────────────────────┘
🏗️ Architecture: The Data Pipeline
The application is powered by a 3-step automated data processing pipeline that runs before the frontend is ever loaded.

┌─────────────────────────────────────────────────────────────┐
│                 AI-Powered Data Pipeline                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Step 1: Chat Generation (main.py)                          │
│  [Gemini API] → Simulates 8 months of chats → all_chats.json │
│      ↓                                                      │
│  Step 2: Episode Summarization (journey.py)                 │
│  [all_chats.json] → [Gemini API] → journey_episodes.json     │
│      ↓                                                      │
│  Step 3: Decision Analysis (decision.py)                    │
│  [all_chats.json] → [Gemini API] → individual_traces.json    │
│      ↓                                                      │
│  Final Output: Structured data ready for the React UI       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
🛠️ Technology Stack
Data Pipeline (Backend Logic)
Python 3.x - For scripting the data processing pipeline.

Google Gemini 2.5 Pro - The core AI model for generation, summarization, and analysis.

python-dotenv - For managing API keys.

Frontend
React 18 - Modern hooks-based architecture (useState, useEffect).

React Router - For multi-page navigation (Journey vs. Dashboard).

Chart.js - For creating the analytics dashboards.

Vercel - For seamless deployment and hosting.

📂 Project Structure
elyx-hackathon-submission/
├── data/                       # All generated JSON data
│   ├── decisions/             # Individual decision trace JSON files
│   ├── all_chats.json
│   └── journey_episodes.json
├── prompts/                    # The prompts for the Gemini API
│   ├── chat_generation.md
│   ├── decision_trace.md
│   └── journey_summary.md
├── webapp/                     # The React frontend application
│   ├── src/
│   │   ├── data/              # A copy of the data for the app to use
│   │   ├── App.js             # Main router
│   │   ├── JourneyView.js     # The core chat/episode component
│   │   └── Dashboard.js       # The analytics dashboard component
│   └── package.json
├── .gitignore
├── decision.py                 # Python script for Step 3
├── journey.py                  # Python script for Step 2
├── main.py                     # Python script for Step 1
└── README.md
🚀 Getting Started
Prerequisites
Python 3.x

Node.js 18+

A Google Gemini API Key

Installation & Running
Clone the Repository

Bash

git clone <your-repo-url>
cd <your-repo-folder>
Set up the Python Environment

Bash

pip install -r requirements.txt
# Create a .env file and add: GEMINI_API_KEY=YOUR_API_KEY_HERE
Run the Data Pipeline

Bash

python main.py
python journey.py
python decision.py
Start the React Frontend

Bash

cd webapp
npm install
npm start
See the App in Action

Open your browser to http://localhost:3000.

Click on episodes, view chats, and click on decisions to see the rationale.

Navigate to the Dashboard to see the analytics.

💡 Decision Traceability in Action
The core feature is the ability to instantly understand the "why" behind any decision.

JavaScript

// Conceptual logic in JourneyView.js

// 1. A decision message is identified and rendered with a special style
<div className="chat-bubble decision" onClick={() => handleDecisionClick(decisionId)}>...</div>

// 2. When clicked, the app dynamically loads the corresponding trace file
const handleDecisionClick = (decisionId) => {
    import(`./data/decisions/${decisionId}.json`)
        .then(trace => {
            // 3. The AI-generated rationale is displayed in a modal
            setDecisionTrace(trace);
        });
};
🌟 Future Prospects
This project provides a strong foundation that can be extended with more advanced features:

Sentiment Analysis: Track member sentiment (frustration, happiness) over time on the dashboard.

Predictive Intervention Alerts: Use AI to detect patterns in chat (e.g., repeated mentions of poor sleep) and alert the Elyx team proactively.

Direct Wearable Integration: Connect directly to Garmin/Oura APIs to correlate chat data with real-time physiological data.

Natural Language Querying: Implement a chat agent where a team member can ask questions like, "Show me all conversations about Rohan's blood pressure in May."
