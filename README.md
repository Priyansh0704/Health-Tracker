<h1 align="center">Elyx Health Journey Visualizer</h1>
<p align="center"><i>A submission for the Elyx Hackathon (August 2025)</i></p>

---

<p align="center">
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
<img src="https://img.shields.io/badge/Node.js-339933?style=for-the-badge&logo=node.js&logoColor=white" alt="Node.js">
<img src="https://img.shields.io/badge/Gemini%20Pro-8E77F0?style=for-the-badge&logo=google-gemini&logoColor=white" alt="Gemini Pro">
<img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" alt="React">
<img src="https://img.shields.io/badge/React%20Router-CA4245?style=for-the-badge&logo=react-router&logoColor=white" alt="React Router">
<img src="https://img.shields.io/badge/Chart.js-FF6384?style=for-the-badge&logo=chartdotjs&logoColor=white" alt="Chart.js">
<img src="https://img.shields.io/badge/Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white" alt="Vercel">
</p>

---

### 🚀 Live Demo
👉 [Click here to view the deployed app](https://health-tracker-2v06sytld-priyansh-goyals-projects.vercel.app/)

---

### ✨ What is the Health Journey Visualizer?
The **Health Journey Visualizer** is an interactive, AI-powered tool that transforms **8 months of raw chat logs** into a structured, interactive timeline.  

It helps the Elyx team analyze member engagement, **pinpoint key events**, and understand the **“why”** behind every decision.

---

### 🔑 Key Features
- **AI-Generated Journey Episodes** → Weekly summaries of raw chat logs.  
- **Interactive Chat Timeline** → Drill down into conversations week by week.  
- **One-Click Decision Traceability** → See rationale for every decision.  
- **Analytics Dashboards** → Visualize trends like stress, adherence, and engagement.  
- **Modern React Frontend** → Responsive, clean UI with Chart.js.  
- **Automated Data Pipeline** → Python + Gemini API for processing.  

---

### 💡 Why This Project Matters
Most health platforms show *what* was done.  
This tool reveals *why* it was done.  

It turns **chaotic, unstructured chat data** into **clear, actionable insights**.

---

### 📊 From Data Chaos to Clarity

| **Raw Data (Before)** | **Structured Insights (After)** |
|------------------------|---------------------------------|
| 2000+ JSON messages | 32 AI-summarized weekly episodes |
| No inherent structure or context | 15+ AI-analyzed decision traces |
| Hard to find key decisions | One-click rationale access |
| Rationale buried in chat | Visual dashboards for instant analysis |

✅ **95%+ reduction in analysis time**

---

### 🏗️ Architecture: The Data Pipeline

```text
┌─────────────────────────────────────────────────────────────┐
│                 AI-Powered Data Pipeline                    │
├─────────────────────────────────────────────────────────────┤
│ Step 1: Chat Generation (main.py)                           │
│   Gemini → 8 months chats → all_chats.json                  │
│                                                             │
│ Step 2: Episode Summarization (journey.py)                  │
│   all_chats.json → Gemini → journey_episodes.json           │
│                                                             │
│ Step 3: Decision Analysis (decision.py)                     │
│   all_chats.json → Gemini → individual_traces.json          │
│                                                             │
│ Final Output → Structured data for React UI                 │
└─────────────────────────────────────────────────────────────┘
```

🛠️ Technology Stack
Backend / Data Pipeline
<p> <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"> <img src="https://img.shields.io/badge/Gemini%20Pro-8E77F0?style=for-the-badge&logo=google-gemini&logoColor=white" alt="Gemini Pro"> <img src="https://img.shields.io/badge/dotenv-000000?style=for-the-badge&logo=dotenv&logoColor=white" alt="dotenv"> </p>
Frontend
<p> <img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" alt="React"> <img src="https://img.shields.io/badge/React%20Router-CA4245?style=for-the-badge&logo=react-router&logoColor=white" alt="React Router"> <img src="https://img.shields.io/badge/Chart.js-FF6384?style=for-the-badge&logo=chartdotjs&logoColor=white" alt="Chart.js"> <img src="https://img.shields.io/badge/Node.js-339933?style=for-the-badge&logo=node.js&logoColor=white" alt="Node.js"> <img src="https://img.shields.io/badge/Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white" alt="Vercel"> </p>

📂 Project Structure
```
elyx-hackathon-submission/
├── data/                       # Generated JSON data
│   ├── decisions/              # Individual decision traces
│   ├── all_chats.json
│   └── journey_episodes.json
├── prompts/                    # Gemini prompts
│   ├── chat_generation.md
│   ├── decision_trace.md
│   └── journey_summary.md
├── webapp/                     # React frontend
│   ├── src/
│   │   ├── data/               # Local copy of data
│   │   ├── App.js              # Main router
│   │   ├── JourneyView.js      # Chat/episode timeline
│   │   └── Dashboard.js        # Analytics dashboard
│   └── package.json
├── main.py                     # Step 1: Chat generation
├── journey.py                  # Step 2: Episode summarization
├── decision.py                 # Step 3: Decision analysis
└── README.md
```
🚀 Getting Started
Prerequisites
Python 3.x

Node.js 18+

Google Gemini API Key

Setup
bash
Copy
Edit
# Clone the repo
git clone <your-repo-url>
cd <your-repo-folder>

# Install backend dependencies
pip install -r requirements.txt

# Add API key
echo "GEMINI_API_KEY=YOUR_API_KEY_HERE" > .env
Run Data Pipeline
bash
Copy
Edit
python main.py
python journey.py
python decision.py
Start Frontend
bash
Copy
Edit
cd webapp
npm install
npm start
Open 👉 http://localhost:3000



💡 Decision Traceability in Action
```javascript
// In JourneyView.js

// 1. Mark decision messages with special style
<div className="chat-bubble decision" 
     onClick={() => handleDecisionClick(decisionId)}>...</div>

// 2. Load corresponding trace file dynamically
const handleDecisionClick = (decisionId) => {
    import(`./data/decisions/${decisionId}.json`)
        .then(trace => setDecisionTrace(trace));
};
```
### 🌟 Future Prospects
Sentiment Analysis → Track frustration/happiness trends.

Predictive Alerts → Detect early warning signs (e.g., sleep issues).

Wearable Integration → Sync Garmin/Oura data with chat context.

Natural Language Querying → Ask: “Show me all conversations about Rohan’s BP in May.”

