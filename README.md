Elyx Health Journey Visualizer
A submission for the Elyx Hackathon (August 2025)
This project provides an interactive visualization of a member's 8-month health journey with Elyx. It transforms raw, unstructured chat logs into a clear, actionable timeline, allowing the Elyx team to track progress and understand the critical "why" behind every decision made.

🚀 Live Demo
You can access the live, deployed web application here:

https://your-deployment-link-goes-here.vercel.app/

✨ Core Features
Interactive Journey Timeline: View a high-level summary of the member's journey, broken down into weekly, AI-generated "episodes."

Detailed Conversation View: Click on any episode to see the complete, time-stamped chat history between the member and the Elyx team for that period.

Decision Traceability: The key feature of the application. Click on any highlighted [DECISION] message to instantly see a pop-up modal explaining the trigger, rationale, and owner of that decision, based on the preceding conversations.

Analytics Dashboards:

Member Health Dashboard: Tracks trends in adherence, missed workouts, and mentions of stress over the 8-month period.

Internal Metrics Dashboard: Visualizes the engagement distribution among the different Elyx team members.

🛠️ Technology Stack
Data Generation: Python, Google Gemini API (gemini-2.5-pro)

Frontend: React, React Router, Chart.js

Deployment: Vercel

⚙️ How It Works
The project follows a three-step data processing pipeline to create the final visualization:

Chat Generation (main.py): An AI-powered script simulates an 8-month WhatsApp conversation between the member (Rohan Patel) and the Elyx team, based on a detailed prompt. This generates a raw all_chats.json file.

Journey Episode Generation (journey.py): This script reads the raw chat log, groups messages into weekly chunks, and uses the Gemini API to summarize each week into a structured "episode." This creates the journey_episodes.json file.

Decision Trace Generation (decision.py): The script scans the chat logs for [DECISION] tags. For each decision, it gathers the "driver" messages and uses the Gemini API to generate a detailed rationale, which is saved as a separate JSON file.

The React web application then consumes these pre-processed JSON files to render the interactive UI.

🖥️ How to Run Locally
To run this project on your local machine, you will need to run the data generation scripts first, and then start the web application.

Prerequisites
Python 3.x

Node.js and npm

A Google Gemini API key

1. Setup the Python Environment
First, set up the Python scripts to generate the data.

Bash

# Clone the repository
git clone <your-repo-url>
cd <your-repo-folder>

# Install Python dependencies
pip install -r requirements.txt

# Create a .env file in the root directory
# and add your Gemini API key to it:
# GEMINI_API_KEY=YOUR_API_KEY_HERE
2. Generate the Data
Run the Python scripts in order.

Bash

# 1. Generate the raw chat logs
python main.py

# 2. Generate the structured journey episodes
python journey.py

# 3. Generate the decision traces
python decision.py
This will populate the ./data folder with all the necessary JSON files.

3. Run the React Web Application
Now, start the frontend application.

Bash

# Navigate into the webapp directory
cd webapp

# Install frontend dependencies
npm install

# Start the development server
npm start
Your browser should automatically open to http://localhost:3000, where you can see the running application.
