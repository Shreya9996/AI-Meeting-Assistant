🎬 AI Meeting Assistant

Turn long meetings into clear, searchable, and actionable knowledge.

An AI-powered meeting analysis system that converts meeting audio/video into a structured knowledge base. It uses Whisper for speech-to-text, Mistral for intelligent analysis, ChromaDB for vector storage, and RAG for asking questions about the meeting.

✨ Project Overview

The AI Meeting Assistant takes a YouTube meeting/video URL or a local audio/video file and processes it through an AI pipeline.

The system can:

🎧 Download and process meeting audio

✂️ Split long audio into manageable chunks

🎙️ Transcribe audio using local OpenAI Whisper

🏷️ Generate a professional meeting title

📝 Generate a meeting summary

📌 Extract action items

🔑 Extract key decisions

❓ Extract unresolved questions

🧠 Build a ChromaDB vector store from the transcript

💬 Answer questions using Retrieval-Augmented Generation (RAG)

🌐 Support English / Hinglish workflow input

🖥️ Provide a Streamlit UI for a modern user experience

🚀 Key Features

Feature

Technology

🎥 YouTube / Local Audio Input

yt-dlp, pydub

🎙️ Speech-to-Text

OpenAI Whisper

🔊 Audio Processing

FFmpeg + Pydub

🧠 LLM Analysis

Mistral

📝 Summarization

LangChain + Mistral

📌 Action Item Extraction

LangChain + Mistral

🔑 Decision Extraction

LangChain + Mistral

❓ Question Extraction

LangChain + Mistral

🔍 Semantic Search

ChromaDB

🧩 Embeddings

HuggingFace Sentence Transformers

💬 Meeting Q&A

RAG + Mistral

🖥️ UI

Streamlit

🏗️ System Architecture

                         🎬 AI MEETING ASSISTANT
                                  │
                                  ▼
                    ┌─────────────────────────┐
                    │     Input Source        │
                    │                         │
                    │ YouTube URL / Local     │
                    │ Audio / Video File      │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │    Audio Processing     │
                    │   yt-dlp + FFmpeg       │
                    │       + Pydub           │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │      Audio Chunking      │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │       Whisper STT        │
                    │   Speech → Transcript    │
                    └────────────┬────────────┘
                                 │
                ┌────────────────┼─────────────────┐
                │                │                 │
                ▼                ▼                 ▼
        🏷️ Title          📝 Summary        📌 Action Items
                │                │                 │
                └────────────────┼─────────────────┘
                                 │
                         ┌───────┴────────┐
                         ▼                ▼
                  🔑 Decisions      ❓ Questions
                         │                │
                         └───────┬────────┘
                                 ▼
                    ┌─────────────────────────┐
                    │       ChromaDB           │
                    │   Vector Knowledge Base  │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │       RAG Retriever      │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │       Mistral LLM        │
                    └────────────┬────────────┘
                                 │
                                 ▼
                         💬 Meeting Q&A

📂 Project Structure

Video Agent/
│
├── main.py
├── app.py
├── requirements.txt
├── .env
├── README.md
│
├── core/
│   ├── transcriber.py
│   ├── summarizer.py
│   ├── extractor.py
│   ├── rag_engine.py
│   └── vector_store.py
│
├── utils/
│   └── audio_processor.py
│
├── downloades/
│   └── # processed audio files
│
└── vector_db/
    └── # ChromaDB persistent storage

🧩 Core Modules

main.py

The main orchestration layer.

It connects:

Audio Processing
      ↓
Transcription
      ↓
Title + Summary
      ↓
Action Items
      ↓
Key Decisions
      ↓
Open Questions
      ↓
RAG Knowledge Base

The main pipeline returns:

{
    "title": title,
    "transcript": transcript,
    "summary": summary,
    "action_items": action_items,
    "key_decisions": decisions,
    "open_questions": questions,
    "rag_chain": rag_chain
}

core/transcriber.py

Responsible for:

Loading Whisper

Transcribing audio chunks

Combining chunk transcriptions

core/summarizer.py

Responsible for:

Meeting title generation

Meeting summarization

core/extractor.py

Responsible for extracting:

Action items

Key decisions

Open questions

core/vector_store.py

Responsible for:

Creating embeddings

Splitting transcript into chunks

Creating ChromaDB vector storage

Loading the vector store

Creating the retriever

core/rag_engine.py

Responsible for:

User Question
     ↓
Retriever
     ↓
Relevant Transcript Chunks
     ↓
Prompt
     ↓
Mistral
     ↓
Answer

utils/audio_processor.py

Responsible for:

Detecting YouTube URLs

Downloading audio

Converting audio

Chunking audio

app.py

Streamlit presentation layer.

The UI uses the existing backend pipeline instead of duplicating the AI logic.

⚙️ Requirements

Software

Python 3.10+

FFmpeg

Mistral API key

Internet connection for model/API downloads and YouTube processing

Python Packages

The project uses packages including:

yt-dlp
pydub
ffmpeg-python

openai-whisper
torch
torchaudio

deep-translator

langchain
langchain-core
langchain-community
langchain-mistralai
mistralai

chromadb
langchain-chroma
sentence-transformers
langchain-huggingface
huggingface-hub
tiktoken

streamlit
streamlit-extras
watchdog

reportlab
fpdf2

python-dotenv
numpy
tqdm
requests

Install the project's dependencies with:

uv pip install -r requirements.txt

🔧 FFmpeg Setup

FFmpeg is required for audio extraction and conversion.

Verify installation:

ffmpeg -version

Also verify:

ffprobe -version

Both commands should return FFmpeg information.

If PowerShell cannot find FFmpeg after installation, restart the terminal and try again.

🔐 Environment Variables

Create a .env file in the project root:

MISTRAL_API_KEY="your_mistral_api_key"
WHISPER_MODEL="small"

⚠️ Security

Do not commit .env to GitHub.

Add it to .gitignore:

.env
.venv/
__pycache__/
downloades/
vector_db/
*.pyc

▶️ Run the CLI Application

Activate the virtual environment:

.venv\Scripts\Activate.ps1

Then run:

python main.py

The application will ask for:

🎥 Enter YouTube URL or local file path:
🌐 Language (english/hinglish):

After processing, it displays:

🏷️ TITLE
📝 SUMMARY
📌 ACTION ITEMS
🔑 KEY DECISIONS
❓ OPEN QUESTIONS

Then the meeting becomes available through:

💬 MEETING CHAT

🖥️ Run the Streamlit UI

If app.py has been created:

streamlit run app.py

Streamlit will open the application in your browser.

The intended flow is:

🎬 Dashboard
      ↓
🎥 Enter URL / Upload File
      ↓
🌐 Select Language
      ↓
🚀 Analyze Meeting
      ↓
🎙️ Whisper Transcription
      ↓
🧠 Mistral Analysis
      ↓
🔎 ChromaDB + RAG
      ↓
📊 Meeting Analysis
      ↓
💬 Ask Meeting

💬 Example Questions

After a meeting has been processed, users can ask questions such as:

What were the main topics discussed?

What is an AI Agent?

What is the difference between AI Agents and Large Reasoning Models?

How are vector databases used in RAG?

What is Model Context Protocol?

What were the key decisions?

What action items were mentioned?

The RAG system should answer using the relevant meeting transcript content.

For information that is not available in the transcript, the configured RAG prompt instructs the assistant to indicate that the information could not be found in the meeting transcript.

🧠 RAG Pipeline

The RAG implementation follows:

Meeting Transcript
        ↓
RecursiveCharacterTextSplitter
        ↓
Transcript Chunks
        ↓
HuggingFace Embeddings
        ↓
ChromaDB
        ↓
Similarity Retriever
        ↓
Relevant Context
        ↓
Mistral
        ↓
Meeting Answer

This allows users to ask natural-language questions about long meetings without manually searching through the entire transcript.

🎯 Why This Project?

Long meetings contain valuable information, but manually reviewing recordings and transcripts is time-consuming.

The AI Meeting Assistant helps convert unstructured meeting recordings into:

Structured summaries

Actionable tasks

Important decisions

Follow-up questions

Searchable meeting knowledge

Instead of watching an entire recording again, users can simply ask:

"What did we decide about the project?"

or:

"What are the pending action items?"

🛠️ Technology Stack

AI / ML

OpenAI Whisper

Mistral Small

HuggingFace Sentence Transformers

LLM Framework

LangChain

LangChain LCEL

Vector Database

ChromaDB

Audio

FFmpeg

Pydub

yt-dlp

Frontend

Streamlit

Programming Language

Python

🔮 Future Enhancements

Possible future improvements include:

👥 Speaker diarization

⏱️ Timestamp-based transcript navigation

📊 Meeting analytics dashboard

📧 Email summary generation

📅 Calendar integration

📄 Automatic meeting report generation

🔊 Support for more audio/video sources

🌍 More multilingual transcription and translation

☁️ Cloud deployment

👤 User authentication

💾 Multiple meeting history

🔎 Search across multiple meetings

📱 Responsive web interface

⚠️ Notes

Whisper Performance

Local Whisper models can be computationally expensive on CPU. Longer meetings may take significant time to transcribe.

The configured model is controlled through:

WHISPER_MODEL="small"

YouTube Processing

YouTube extraction depends on yt-dlp, FFmpeg, and the availability of the requested media stream. YouTube changes can occasionally affect downloading.

API Usage

Mistral API calls are used for title generation, summarization, extraction, and RAG responses.

Keep your API key private.

📜 License

This project is currently intended as a personal/educational AI project.

Add an appropriate open-source license before public redistribution.

👩‍💻 Author

Shreya Patil

B.Tech Computer Science StudentAI/ML • Data Science • Generative AI • Python

⭐ Project Vision

From meeting recordings to meeting intelligence — automatically.

🎙️ Transcribe → 🧠 Understand → 📌 Extract → 🔎 Retrieve → 💬 Ask
