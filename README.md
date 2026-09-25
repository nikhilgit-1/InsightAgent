# 🚀 InsightAgent: Dynamic Multi-Database AI Analytics Assistant

<p align="center">
  <img src="frontend/src/assets/hero.png" alt="InsightAgent Hero" width="100%" />
</p>

**InsightAgent** is an advanced, enterprise-grade full-stack AI application designed to bridge the gap between natural language and complex database analytics. Powered by **Google Gemini API**, **LangGraph**, **FastAPI**, and a sleek **React/Vite** frontend, it empowers users to interact conversationally with relational and non-relational databases through autonomous tool selection and intelligent reasoning.

---

## 🔥 Core Highlights & Key Features

- **Dynamic Database Connectivity:** Unlike rigid static applications, InsightAgent allows users to dynamically connect and query their own databases (SQLite, MySQL, etc.) at runtime without any hardcoded structural dependencies.
- **Autonomous Agentic Reasoning (`setup_db.py` & `setup_nosql.py`):** Dedicated testing and initialization scripts were utilized to rigorously train and test the AI agent's reasoning capabilities, ensuring it autonomously decides when and how to invoke specific SQL or NoSQL tools.
- **Robust Security & Environment Isolation:** 
  - Sensitive configuration keys and credentials are strictly isolated using `.env` files and guarded by comprehensive `.gitignore` and `.dockerignore` policies to prevent any public exposure.
  - Built-in fault-tolerant error handling and rate-limit mitigation (`429 Too Many Requests`) ensure the application remains stable and user-friendly under heavy operational loads.
- **API Scalability (Free & Paid Tiers):** Built on top of the Google Gemini API. While the free tier accommodates standard exploration, the architecture easily scales for heavy daily production workloads by simply swapping in a paid Gemini API key.

---

## 🛠️ Tech Stack & Architecture

- **Frontend:** React, Vite, Tailwind CSS, Axios
- **Backend:** Python, FastAPI, Uvicorn, SQLAlchemy
- **AI & Agentic Framework:** Google Gemini (Gemini Flash), LangChain, LangGraph (ReAct agent architecture)
- **Containerization:** Docker & Docker Compose (Multi-container secure isolation)

---

## 📂 Project Repository Structure

```text
InsightAgent/
├── frontend/               # React + Vite frontend application
│   ├── src/                # UI Components (ChatInterface, DbConnectionManager)
│   ├── Dockerfile          # Frontend container configuration
│   └── .dockerignore       # Optimizing Docker context for Vite
├── assets/                 # Architecture diagrams, testing snapshots & UI outputs
├── agent.py                # Core LangGraph AI Agent & dynamic tool-calling logic
├── main.py                 # FastAPI backend server & secure API endpoints
├── business_data.db        # Default SQLite business intelligence database
├── setup_db.py             # Script to provision and seed SQLite for agent testing
├── setup_nosql.py          # Script for NoSQL/MongoDB engine testing & structures
├── Dockerfile              # Backend Python container configuration
├── docker-compose.yml      # Orchestrates FastAPI & React containers
├── .env.example            # Template for environment variables & API configuration
└── requirements.txt        # Python backend dependencies

🐳 Running the Project via Docker (Recommended)
Thanks to containerization, you do not need to configure complex local environments. Everything runs inside secure, isolated Docker containers.

Quick Start Guide
Clone the repository:

Bash
git clone [https://github.com/nikhilgit-1/InsightAgent.git](https://github.com/nikhilgit-1/InsightAgent.git)
cd InsightAgent
Configure Environment Variables:
Copy .env.example to create your local .env file:

Bash
cp .env.example .env
Open .env and provide your active Google Gemini API Key:

Code snippet
GEMINI_API_KEY=your_actual_gemini_api_key_here
Build and Run with Docker Compose:

Bash
docker-compose up --build
Access the Application:

Frontend UI: http://localhost:5173

Backend API Documentation (Swagger UI): http://localhost:8000/docs

💻 Manual Local Setup (Without Docker)
If you prefer running the application directly on your local machine for development:

1. Backend Setup (FastAPI)
Bash
pip install -r requirements.txt
python setup_db.py
uvicorn main:app --reload --port 8000
2. Frontend Setup (React/Vite)
Bash
cd frontend
npm install
npm run dev
(Access the app at http://localhost:5173)

📜 License
This project is open-source and available under the MIT License.

Copyright (c) 2026 Nikhil Kumar