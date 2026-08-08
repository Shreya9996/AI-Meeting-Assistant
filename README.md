🎬 AI Meeting Assistant

Turn long meetings into clear, searchable, and actionable knowledge.

An AI-powered meeting assistant that converts a YouTube URL or local audio/video into a structured meeting analysis using Whisper + Mistral + LangChain + ChromaDB + RAG.

✨ What It Does

🎥 Input meeting video/audio→ 🎧 Extract & process audio→ ✂️ Split audio into chunks→ 🎙️ Whisper transcription→ 🧠 Mistral analysis→ 🏷️ Title + 📝 Summary→ 📌 Action Items + 🔑 Decisions + ❓ Open Questions→ 🗄️ ChromaDB vector store→ 🔎 RAG retrieval→ 💬 Ask questions about the meeting

🏗️ Project Flowchart

              🎬 AI MEETING ASSISTANT
                       │
                       ▼
        ┌─────────────────────────────┐
        │ 🎥 YouTube / Local File    │
        └──────────────┬──────────────┘
                       ▼
        ┌─────────────────────────────┐
        │ 🎧 Audio Processing         │
        │ yt-dlp + FFmpeg + Pydub    │
        └──────────────┬──────────────┘
                       ▼
        ┌─────────────────────────────┐
        │ ✂️ Audio Chunking           │
        └──────────────┬──────────────┘
                       ▼
        ┌─────────────────────────────┐
        │ 🎙️ Whisper STT              │
        │ Speech → Transcript         │
        └──────────────┬──────────────┘
                       ▼
        ┌─────────────────────────────┐
        │ 🧠 Mistral + LangChain      │
        └──────────────┬──────────────┘
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
       🏷️ Title    📝 Summary   📌 Actions
                       │
                ┌──────┴──────┐
                ▼             ▼
          🔑 Decisions    ❓ Questions
                │             │
                └──────┬──────┘
                       ▼
        ┌─────────────────────────────┐
        │ 🗄️ ChromaDB + Embeddings   │
        └──────────────┬──────────────┘
                       ▼
                🔎 RAG Retriever
                       │
                       ▼
                 🤖 Mistral LLM
                       │
                       ▼
                  💬 Meeting Q&A

🧩 Project Structure

Video Agent/
│
├── main.py                  # Main pipeline + CLI
├── app.py                   # Streamlit UI
├── requirements.txt
├── .env
│
├── core/
│   ├── transcriber.py       # Whisper transcription
│   ├── summarizer.py        # Title + summary
│   ├── extractor.py         # Actions, decisions, questions
│   ├── vector_store.py      # Embeddings + ChromaDB
│   └── rag_engine.py        # RAG question answering
│
├── utils/
│   └── audio_processor.py   # Download, convert, chunk audio
│
├── downloades/              # Processed audio
└── vector_db/               # ChromaDB storage

🛠️ Tech Stack

Layer

Technology

Language

Python

Audio

FFmpeg, Pydub, yt-dlp

Speech-to-Text

OpenAI Whisper

LLM

Mistral Small

Framework

LangChain / LCEL

Embeddings

HuggingFace Sentence Transformers

Vector DB

ChromaDB

UI

Streamlit

🧠 RAG in This Project

Meeting Transcript
       ↓
Text Chunks
       ↓
HuggingFace Embeddings
       ↓
ChromaDB
       ↓
Similarity Search
       ↓
Relevant Transcript
       ↓
Mistral
       ↓
💬 Answer

The assistant answers questions using the relevant meeting transcript content instead of manually searching the complete transcript.

▶️ Run

.venv\Scripts\Activate.ps1
python main.py

For Streamlit:

streamlit run app.py

🔐 .env

MISTRAL_API_KEY="your_mistral_api_key"
WHISPER_MODEL="small"

Keep your API key private and do not commit .env to GitHub.

🎯 Example Questions

What were the main topics discussed?

What is an AI Agent?

What is the difference between AI Agents and Large Reasoning Models?

What were the key decisions?

What action items were mentioned?

How is RAG used in the meeting?

🚀 Project Vision

🎙️ Transcribe → 🧠 Understand → 📌 Extract → 🔎 Retrieve → 💬 Ask

Built as an AI/ML project demonstrating speech-to-text, LLM orchestration, vector databases, and RAG-based question answering.
