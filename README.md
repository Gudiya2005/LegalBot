# 🛡️ LegalBot
- Login alerts


### 📄 Complaint Draft
Helps users prepare structured cyber crime complaint drafts by collecting relevant incident information and generating a formal draft for review.


### 🎙️ Voice Input
- Voice-based message input
- Audio recording through the browser
- Whisper-based speech-to-text transcription
- Transcribed text is placed directly into the chat input


### 🗂️ Conversation History
- Stores user conversations
- Allows users to view recent chats
- Allows users to reopen previous conversations
- Maintains conversation and tool information


### 🔐 Authentication
- User registration
- User login
- JWT-based authentication
- Protected API endpoints
- User-specific chat history


### 🌓 Light & Dark Mode
- Cyber-security inspired interface
- Light mode
- Dark mode
- Responsive chat interface
- Modern sidebar and agent navigation


---


# 🧠 System Architecture


```text
                         ┌──────────────────┐
                         │      User        │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │ React Frontend   │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │  FastAPI Backend │
                         └────────┬─────────┘
                                  │
                                  ▼
                       ┌─────────────────────┐
                       │ Agent Orchestration │
                       └──────────┬──────────┘
                                  │
              ┌───────────────────┼───────────────────┐
              │                   │                   │
              ▼                   ▼                   ▼
       ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
       │ Gemini Brain│     │ Scam Checker│     │  Emergency  │
       │    Agent    │     │    Agent    │     │    Agent    │
       └──────┬──────┘     └─────────────┘     └─────────────┘
              │
              ├──────────────────────┐
              │                      │
              ▼                      ▼
       ┌─────────────┐        ┌──────────────┐
       │ RAG Pipeline│        │ Knowledge    │
       │             │◄───────│    Base      │
       └──────┬──────┘        └──────────────┘
              │
              ▼
       ┌─────────────────┐
       │ Gemini AI Model │
       └────────┬────────┘
                │
                ▼
       ┌────────────────────┐
       │ Response Formatter │
       └─────────┬──────────┘
                 │
                 ▼
             User Response


# 🤖 AI Agents

LegalBot uses specialized agents for different cyber safety tasks.

Agent	Purpose
Gemini Cyber Brain	Main cyber crime reasoning and response generation
Scam Checker	Scam and phishing risk analysis
Emergency Agent	Immediate cyber crime safety guidance
Evidence Agent	Digital evidence preservation guidance
Complaint Agent	Cyber crime complaint drafting
Response Formatter	Formats and structures generated responses
📚 RAG Pipeline

LegalBot uses Retrieval-Augmented Generation (RAG) to provide relevant information from its cyber crime knowledge base.

Knowledge Base
      │
      ▼
Document Loading
      │
      ▼
Text Splitting
      │
      ▼
Embeddings
      │
      ▼
Vector Database
      │
      ▼
Relevant Document Retrieval
      │
      ▼
Context + User Query
      │
      ▼
Gemini AI
      │
      ▼
Final Response

The knowledge base contains cyber crime information related to topics such as:

Phishing
OTP Fraud
UPI Fraud
Identity Theft
Fake Loan Scams
Social Media Hacking
🎙️ Voice Processing

LegalBot uses a Whisper-based speech recognition pipeline for voice input.

User Voice
    │
    ▼
Browser Microphone
    │
    ▼
Audio Recording
    │
    ▼
FastAPI Voice Endpoint
    │
    ▼
Whisper Model
    │
    ▼
Text Transcription
    │
    ▼
Chat Input
🛠️ Technology Stack
Frontend
React
Vite
JavaScript
CSS
Backend
Python
FastAPI
SQLAlchemy
SQLite
JWT Authentication
AI / GenAI
Google Gemini
Retrieval-Augmented Generation (RAG)
Embeddings
Vector Database
Faster-Whisper
Development Tools
Visual Studio Code
Git
GitHub
📁 Project Structure
LegalBot/
│
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   ├── api/
│   │   ├── auth/
│   │   ├── database/
│   │   ├── models/
│   │   ├── orchestrator/
│   │   ├── prompts/
│   │   ├── rag/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── templates/
│   │   ├── utils/
│   │   ├── config.py
│   │   └── main.py
│   │
│   ├── knowledge_base/
│   ├── uploads/
│   ├── vector_db/
│   └── requirements.txt
│
├── frontend/
│   ├── public/
│   ├── src/
│   ├── package.json
│   ├── package-lock.json
│   └── vite.config.js
│
├── .gitignore
└── README.md
⚙️ Installation
1. Clone the Repository
git clone https://github.com/your-username/LegalBot.git
cd LegalBot
🐍 Backend Setup

Open a terminal and navigate to the backend:

cd backend

Create a virtual environment:

python -m venv venv

Activate the virtual environment on Windows:

venv\Scripts\activate

Install the required dependencies:

pip install -r requirements.txt
🔐 Environment Variables

Create a .env file inside the backend directory.

Use the following format:

APP_NAME=LegalBot
APP_VERSION=1.0.0


SECRET_KEY=your_secret_key
DATABASE_URL=sqlite:///./legalbot.db
GEMINI_API_KEY=your_gemini_api_key


ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

Important: Never upload your actual .env file or API keys to GitHub.

▶️ Run the Backend

From the backend directory:

uvicorn app.main:app --reload

Backend:

http://127.0.0.1:8000

FastAPI Swagger documentation:

http://127.0.0.1:8000/docs
⚛️ Frontend Setup

Open another terminal:

cd frontend

Install dependencies:

npm install

Start the frontend:

npm run dev

Frontend:

http://localhost:5173
🧪 Testing

The project contains test scripts for different components of the system, including:

Agent pipeline
Chat history
Chat service
Complaint Agent
Cyber Brain
Embeddings
Gemini API
Language processing
Document loading
Retriever
Text splitter
Vector store
🔒 Security

LegalBot is designed as a cyber crime awareness and assistance platform.

Users should avoid sharing unnecessary sensitive information.

The system does not replace:

Law enforcement authorities
Cyber crime reporting authorities
Banks or financial institutions
Cybersecurity professionals
Professional legal advice
⚠️ Disclaimer

LegalBot provides AI-generated assistance and educational guidance related to cyber crime and online fraud.

It does not replace professional legal advice, cybersecurity professionals, financial institutions, or law enforcement authorities.

Complaint drafts generated by LegalBot are intended for review and should be verified before official submission.

🔮 Future Scope

Future improvements may include:

📎 Screenshot and document analysis
🖼️ Image and OCR processing
📄 PDF/DOCX evidence analysis
🔗 Suspicious URL analysis
📱 Phone number risk analysis
🌐 Improved multilingual voice recognition
🧾 Complaint export to PDF
🔔 Real-time cyber fraud alerts
🚀 Cloud deployment
👩‍💻 Project

LegalBot — AI-Powered Cyber Crime & Online Fraud Assistant

An AI/GenAI project combining conversational AI, RAG, multi-agent orchestration, cyber crime knowledge, voice interaction, and a modern web interface.



### Do this now


1. Go to your **main `LegalBot` folder**.
2. Create `README.md`.
3. Paste the entire content above.
4. Save it.
5. **Don't commit/push anything yet.**


Once that's done, tell me **“README done”** and we'll do the next step: **exactly what to upload and what NOT to upload from your current `backend` and `frontend` folders.**
can u generate a file