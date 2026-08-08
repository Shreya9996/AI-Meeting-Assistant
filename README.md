# 🎬 AI Meeting Assistant

> **Turn long meetings into clear, searchable, and actionable knowledge.**

An AI-powered meeting assistant that converts **YouTube videos or local audio/video files** into structured meeting insights and allows users to ask questions about the meeting using **RAG**.

---

## ✨ Features

- 🎥 YouTube URL / Local Audio-Video Input
- 🎧 Audio Extraction & Processing
- ✂️ Long Audio Chunking
- 🎙️ Speech-to-Text using Whisper
- 🏷️ Automatic Meeting Title
- 📝 AI Meeting Summary
- 📌 Action Item Extraction
- 🔑 Key Decision Extraction
- ❓ Open Question Extraction
- 🗄️ ChromaDB Vector Database
- 🔎 Semantic Search with RAG
- 💬 Ask Questions About the Meeting
- 🖥️ Streamlit UI

---
<img width="1355" height="624" alt="image" src="https://github.com/user-attachments/assets/59fce30d-44fa-4604-9f66-157eb883a410" />


<img width="1360" height="658" alt="image" src="https://github.com/user-attachments/assets/7c595fd3-7bf6-4c2e-aec6-4caad1cf1838" />


<img width="1363" height="670" alt="image" src="https://github.com/user-attachments/assets/a5aba99b-8d6c-420c-bce6-0829becc0e48" />

<img width="1362" height="663" alt="image" src="https://github.com/user-attachments/assets/4ac43ad8-cde0-41fb-b006-b508392f887f" />


## 🏗️ System Architecture

```text
                 🎬 AI MEETING ASSISTANT
                          │
                          ▼
              ┌───────────────────────┐
              │ 🎥 YouTube / Local    │
              │     Audio / Video     │
              └───────────┬───────────┘
                          │
                          ▼
              ┌───────────────────────┐
              │ 🎧 Audio Processing   │
              │ yt-dlp + FFmpeg       │
              │ + Pydub               │
              └───────────┬───────────┘
                          │
                          ▼
              ┌───────────────────────┐
              │ ✂️ Audio Chunking     │
              └───────────┬───────────┘
                          │
                          ▼
              ┌───────────────────────┐
              │ 🎙️ Whisper            │
              │ Speech → Text         │
              └───────────┬───────────┘
                          │
                          ▼
              ┌───────────────────────┐
              │ 🧠 Mistral +          │
              │    LangChain          │
              └───────────┬───────────┘
                          │
            ┌─────────────┼─────────────┐
            │             │             │
            ▼             ▼             ▼
        🏷️ Title      📝 Summary     📌 Actions
            │             │             │
            └─────────────┼─────────────┘
                          │
                    ┌─────┴─────┐
                    ▼           ▼
              🔑 Decisions   ❓ Questions
                    │           │
                    └─────┬─────┘
                          ▼
              ┌───────────────────────┐
              │ 🗄️ ChromaDB          │
              │ Vector Knowledge Base │
              └───────────┬───────────┘
                          │
                          ▼
                  🔎 RAG Retriever
                          │
                          ▼
                  🤖 Mistral LLM
                          │
                          ▼
                    💬 Meeting Q&A
