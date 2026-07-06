# 🧭 Visual Job Coach Agent

**An accessible, voice-first AI agent that helps visually impaired and low-vision job seekers search for jobs, prepare for interviews, and navigate the job application process — hands-free.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Gemini](https://img.shields.io/badge/Google%20Gemini-AI%20Engine-4285F4?logo=google&logoColor=white)](https://ai.google.dev/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](#-license)
[![Status](https://img.shields.io/badge/Status-Active%20Development-yellow)](#)

---

## 📖 Overview

**Visual Job Coach Agent** is an AI-powered career assistant purpose-built for **accessibility**. It combines conversational AI, voice navigation, and screen-reader-friendly design to give visually impaired users an equal, independent way to search for jobs, get resume feedback, and practice interviews — all through natural voice or text interaction.

Rather than bolting accessibility on as an afterthought, this project treats it as a first-class design principle: every core skill (navigation, resume review, interview prep) is built to work seamlessly with assistive technology and speech interfaces.

---

## 🎓 Kaggle Capstone Alignment (Course Concepts)

This project was built for the **Kaggle AI Agents: Intensive Vibe Coding Capstone** under the **Concierge / Freestyle Track**. It implements the following core agentic concepts from the course:

1. **Multi-Agent Orchestration & Core Reasoning:** Driven by `job_agent.py` using Google Gemini, separating complex tasks into specialized modules (Screen Reader Skill, Voice Navigation Skill).
2. **Model Context Protocol (MCP):** Features an integrated Model Context Protocol (MCP) server environment (`tests/test_mcp_server.py`) allowing the agent to securely interface with local job schemas, file systems, and tools.
3. **Dual-Layer Memory Architecture:** Implements distinct short-term conversational context (`session_memory.py`) and long-term user profile preference preservation (`user_memory.py`) to maintain persistent coaching context safely.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🗣️ **Voice-First Interaction** | Full speech-to-text and text-to-speech pipeline so users can operate the agent entirely by voice |
| 🔌 **MCP Server Integration** | Exposes job searching and data retrieval tools via Model Context Protocol standard |
| 🔍 **Screen Reader Skill** | Purpose-built skill that structures and narrates content in a screen-reader-friendly way |
| 🧭 **Voice Navigation Skill** | Lets users navigate app features and job listings using spoken commands |
| 💼 **Intelligent Job Search** | Pulls and filters live job listings through an integrated Job Search API |
| 📄 **Resume Assistance** | Dedicated routes for reviewing and improving resumes |
| 🎤 **Interview Preparation** | Conversational mock-interview support with contextual, role-specific questions |
| 🧠 **Session & User Memory** | Maintains conversation context and user profile across sessions for a personalized experience |
| 🔐 **Security-First Design** | Built-in authentication, rate limiting, input sanitization, and PII redaction |

---



Visual_Job_Coach_Agent/
│
├── agent.py                        # Entry point for the core AI agent
│
├── app/
│   ├── main.py                     # FastAPI application entry point
│   ├── config.py                   # App-wide configuration and environment loading
│   │
│   ├── agents/
│   │   └── job_agent.py            # Core reasoning agent (job search, coaching logic)
│   │
│   ├── memory/
│   │   ├── session_memory.py       # Short-term conversational memory
│   │   └── user_memory.py          # Long-term user profile / preference memory
│   │
│   ├── models/
│   │   ├── job_model.py            # Job data schema
│   │   ├── session_model.py        # Session data schema
│   │   └── user_model.py           # User data schema
│   │
│   ├── routes/
│   │   ├── interview_routes.py     # Interview prep endpoints
│   │   ├── job_routes.py           # Job search endpoints
│   │   ├── resume_routes.py        # Resume review endpoints
│   │   └── voice_routes.py         # Voice input/output endpoints
│   │
│   ├── security/
│   │   ├── auth.py                 # Authentication logic
│   │   ├── input_sanitizer.py      # Sanitizes user input
│   │   ├── pii_redaction.py        # Redacts personally identifiable information
│   │   └── rate_limiter.py         # API rate limiting
│   │
│   ├── services/
│   │   ├── job_api.py              # External job board API integration
│   │   ├── speech_to_text.py       # STT service wrapper
│   │   └── text_to_speech.py       # TTS service wrapper
│   │
│   ├── skills/
│   │   ├── screen_reader_skill.py  # Screen-reader-optimized output formatting
│   │   └── voice_navigation_skill.py # Voice-command navigation logic
│   │
│   └── utils/
│       ├── audio_utils.py          # Audio processing helpers
│       └── validators.py           # Input/data validation helpers
│
├── frontend/
│   └── app.py                      # Frontend application (Streamlit/Flask UI)
│
├── tests/
│   ├── test_agents.py
│   ├── test_mcp_server.py          # Validation suite for Model Context Protocol compliance
│   ├── test_routes.py
│   └── test_security.py
│
├── .env.example                    # Sample environment configuration
└── requirements.txt                # Python dependencies

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+**
- **pip** and **venv**
- A **Google Gemini API key** ([get one here](https://aistudio.google.com/apikey))
- (Optional) API keys for your chosen speech service and job search provider

### 1. Clone the repository

```bash
git clone [https://github.com/charan-d11/Visual_Job_Coach_Agent.git](https://github.com/charan-d11/Visual_Job_Coach_Agent.git)
cd Visual_Job_Coach_Agent
2. Create and activate a virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
3. Install dependencies
pip install -r requirements.txt
4. Configure environment variables
cp .env.example .env      # macOS/Linux
copy .env.example .env    # Windows
# ===== LLM / AI =====
GOOGLE_API_KEY=your_google_api_key_here

# ===== Speech Services =====
SPEECH_API_KEY=your_speech_service_key_here

# ===== Job Search API =====
JOB_API_KEY=your_job_api_key_here
JOB_API_BASE_URL=[https://api.example-jobs.com/v1](https://api.example-jobs.com/v1)

# ===== Security =====
APP_SECRET_KEY=change_this_to_a_long_random_string
API_AUTH_TOKEN=change_this_demo_token

# ===== App Settings =====
APP_ENV=development
APP_HOST=0.0.0.0
APP_PORT=8000
RATE_LIMIT_PER_MINUTE=30
5. Run the backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

The API will be available at:

http://localhost:8000
Interactive API docs (Swagger UI) will be available at:

http://localhost:8000/docs

6. Run the frontend
Bash
cd frontend
python app.py

The project includes a test suite covering agents, routes, security, and MCP server behavior:

Bash
pytest tests/

Run a specific test file:

Bash
pytest tests/test_security.py -v

🔐 Security Notes
This project takes several precautions to keep user data and credentials safe:

Input Sanitization — all user input passes through input_sanitizer.py before processing

PII Redaction — pii_redaction.py strips personally identifiable information from logs/outputs

Rate Limiting — configurable per-minute request limits via RATE_LIMIT_PER_MINUTE

Token-based Auth — protected routes require a valid API_AUTH_TOKEN

If you fork or deploy this project, make sure to:

Generate your own strong APP_SECRET_KEY and API_AUTH_TOKEN

Never commit real API keys — only placeholders belong in .env.example

Rotate any credentials immediately if accidentally exposed

🗺️ Roadmap
[ ] Multi-language voice support

[ ] Browser extension for in-page screen-reader job search

[ ] Resume-to-job matching score

[ ] Mobile app companion

[ ] Expanded interview practice with real-time voice feedback

🤝 Contributing
Contributions are welcome! To contribute:

Fork the repository

Create a feature branch (git checkout -b feature/your-feature)

Commit your changes (git commit -m "Add your feature")

Push to your branch (git push origin feature/your-feature)

Open a Pull Request

Please make sure new features include relevant tests in the tests/ directory.

📜 License
This project is licensed under the MIT License — see the LICENSE file for details.

🙌 Acknowledgements
Built with the mission of making job search and career coaching more accessible for visually impaired job seekers — combining conversational AI, speech technology, and thoughtful accessibility-first design.

Author
Durga Charan Mallick
