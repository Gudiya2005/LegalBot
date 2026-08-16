🛡️ LegalBot

AI-Powered Cyber Crime & Online Fraud Assistant

LegalBot is an AI-powered cyber safety assistant designed to help users understand cyber crime incidents, online fraud, scams, phishing attempts, account hacking, and related digital threats.

It combines Generative AI, Retrieval-Augmented Generation (RAG), multi-agent orchestration, voice interaction, authentication, and conversation history into a modern web-based assistant.

⚠️ Disclaimer: LegalBot provides AI-generated assistance and educational guidance. It does not replace professional legal advice, cybersecurity professionals, financial institutions, or law-enforcement authorities. Complaint drafts should be reviewed and verified before official submission.

✨ Features

🤖 AI Cyber Crime Assistant

Conversational assistance for cyber crime and online fraud situations

Context-aware responses

Cyber safety guidance and recommended actions

Gemini-powered reasoning

🔎 Scam & Phishing Checker

Analyzes suspicious messages, calls, links, and situations

Provides a scam-risk assessment

Identifies common phishing and fraud patterns

Gives practical safety recommendations

🚨 Emergency Help

Provides immediate guidance for urgent cyber crime situations

Helps users understand what actions to take

Highlights important information and evidence to preserve

📄 Complaint Draft

Helps users prepare structured cyber crime complaint drafts by collecting relevant incident information and generating a formal draft for review.

🗂️ Evidence Guide

Provides guidance on preserving useful digital evidence such as screenshots, emails, messages, call logs, transaction information, and login alerts.

🎙️ Voice Input

Voice-based message input

Browser-based audio recording

Faster-Whisper speech-to-text transcription

Transcribed text is placed directly into the chat input

🗂️ Conversation History

Stores user conversations

Displays recent chats

Allows users to reopen previous conversations

Maintains conversation and tool information

🔐 Authentication

User registration

User login

JWT-based authentication

Protected API endpoints

User-specific conversation history

🌓 Light & Dark Mode

Cyber-security inspired interface

Light mode

Dark mode

Responsive chat interface

Modern sidebar and agent navigation

🧠 System Architecture

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

🤖 AI Agents

LegalBot uses specialized agents for different cyber safety tasks.

Agent

Purpose

Gemini Cyber Brain

Main cyber crime reasoning and response generation

Scam Checker

Scam and phishing risk analysis

Emergency Agent

Immediate cyber crime safety guidance

Evidence Agent

Digital evidence preservation guidance

Complaint Agent

Cyber crime complaint drafting

Response Formatter

Formats and structures generated responses

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

The knowledge base contains information related to:

Phishing

OTP Fraud

UPI Fraud

Identity Theft

Fake Loan Scams

Social Media Hacking

Digital Arrest

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
Faster-Whisper Model
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
│   ├── .gitignore
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
├── requirements.txt
└── README.md

⚙️ Installation & Setup

1. Clone the Repository

git clone https://github.com/Gudiya2005/LegalBot.git
cd LegalBot

🐍 2. Backend Setup

cd backend
python -m venv venv

Windows:

venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

🔐 3. Environment Variables

Create a .env file inside the backend directory:

APP_NAME=LegalBot
APP_VERSION=1.0.0

SECRET_KEY=your_secret_key
DATABASE_URL=sqlite:///./legalbot.db
GEMINI_API_KEY=your_gemini_api_key

ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

Important: Never upload your actual .env file or API keys to GitHub.

▶️ 4. Run the Backend

From the backend directory:

uvicorn app.main:app --reload

Backend:

http://127.0.0.1:8000

FastAPI Swagger documentation:

http://127.0.0.1:8000/docs

⚛️ 5. Frontend Setup

Open another terminal:

cd frontend
npm install
npm run dev

Frontend:

http://localhost:5173

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

Potential future improvements include:

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

An AI/GenAI project combining conversational AI, RAG, multi-agent orchestration, cyber crime knowledge, voice interaction, authentication, conversation history, and a modern web interface.
