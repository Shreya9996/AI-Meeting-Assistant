# app.py
# Streamlit UI for AI Meeting Assistant
# Backend pipeline is implemented in main.py
# DO NOT modify main.py

import streamlit as st
from datetime import datetime

from main import run_pipeline  # existing backend pipeline - do not duplicate logic here


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Meeting Assistant",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS - DARK PROFESSIONAL SAAS THEME
# ============================================================

st.markdown(
    """
<style>
    /* ---------- Global ---------- */
    .stApp {
        background: radial-gradient(circle at top left, #12121a 0%, #0b0b10 60%);
        color: #e6e6f0;
    }

    #MainMenu, footer, header {visibility: hidden;}

    h1, h2, h3, h4 {
        font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
        letter-spacing: -0.02em;
    }

    /* ---------- Header banner ---------- */
    .app-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 1.4rem 1.8rem;
        border-radius: 16px;
        background: linear-gradient(135deg, rgba(99,102,241,0.15), rgba(168,85,247,0.10));
        border: 1px solid rgba(148,163,255,0.18);
        margin-bottom: 1.6rem;
    }
    .app-header .title {
        font-size: 1.6rem;
        font-weight: 700;
        margin: 0;
        color: #f4f4ff;
    }
    .app-header .subtitle {
        margin: 0.15rem 0 0 0;
        color: #a8a8c0;
        font-size: 0.92rem;
    }
    .badge-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        padding: 0.35rem 0.85rem;
        border-radius: 999px;
        background: rgba(34,197,94,0.12);
        border: 1px solid rgba(34,197,94,0.35);
        color: #4ade80;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .tech-badges {
        margin-top: 0.6rem;
        font-size: 0.78rem;
        color: #8b8ba8;
        letter-spacing: 0.03em;
    }

    /* ---------- Cards ---------- */
    .card {
        background: rgba(255,255,255,0.035);
        border: 1px solid rgba(148,163,255,0.14);
        border-radius: 14px;
        padding: 1.3rem 1.4rem;
        margin-bottom: 1rem;
    }
    .card h4 {
        margin-top: 0;
        color: #f4f4ff;
    }
    .feature-card {
        background: rgba(255,255,255,0.035);
        border: 1px solid rgba(148,163,255,0.14);
        border-radius: 14px;
        padding: 1.4rem;
        text-align: left;
        height: 100%;
        transition: border-color 0.2s ease;
    }
    .feature-card:hover {
        border-color: rgba(139,92,246,0.55);
    }
    .feature-card .icon {
        font-size: 1.6rem;
        margin-bottom: 0.5rem;
    }
    .feature-card .f-title {
        font-weight: 700;
        color: #f0f0ff;
        margin-bottom: 0.2rem;
    }
    .feature-card .f-sub {
        color: #9797b5;
        font-size: 0.85rem;
    }

    /* ---------- Metric-style stat card ---------- */
    .stat-card {
        background: rgba(255,255,255,0.035);
        border: 1px solid rgba(148,163,255,0.14);
        border-radius: 14px;
        padding: 1.1rem 1.2rem;
        text-align: center;
    }
    .stat-card .stat-value {
        font-size: 1.9rem;
        font-weight: 800;
        background: linear-gradient(135deg, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .stat-card .stat-label {
        color: #9797b5;
        font-size: 0.82rem;
        margin-top: 0.2rem;
    }

    /* ---------- Section title ---------- */
    .section-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #f0f0ff;
        margin: 1.4rem 0 0.6rem 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* ---------- Sidebar ---------- */
    section[data-testid="stSidebar"] {
        background: #0e0e15;
        border-right: 1px solid rgba(148,163,255,0.12);
    }

    /* ---------- Buttons ---------- */
    .stButton > button {
        border-radius: 10px;
        border: 1px solid rgba(148,163,255,0.25);
        background: linear-gradient(135deg, #6366f1, #a855f7);
        color: white;
        font-weight: 600;
        padding: 0.55rem 1rem;
    }
    .stButton > button:hover {
        border-color: rgba(168,85,247,0.6);
        opacity: 0.92;
    }

    hr {
        border-color: rgba(148,163,255,0.12);
    }
</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

if "result" not in st.session_state:
    st.session_state.result = None

if "rag_chain" not in st.session_state:
    st.session_state.rag_chain = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "source" not in st.session_state:
    st.session_state.source = ""

if "language" not in st.session_state:
    st.session_state.language = "english"

if "analysis_completed" not in st.session_state:
    st.session_state.analysis_completed = False

if "last_error" not in st.session_state:
    st.session_state.last_error = None

if "active_page" not in st.session_state:
    st.session_state.active_page = "🏠 Dashboard"


# ============================================================
# HELPERS
# ============================================================

def safe_count(value) -> int:
    """Best-effort count for list/str/dict-like results, without guessing structure."""
    if value is None:
        return 0
    if isinstance(value, (list, tuple, set)):
        return len(value)
    if isinstance(value, dict):
        return len(value)
    if isinstance(value, str):
        # Count non-empty lines as a reasonable proxy for "items" in free text
        lines = [ln for ln in value.splitlines() if ln.strip()]
        return len(lines)
    return 0


def render_block(value):
    """Render list/dict/str content in a readable way inside a card."""
    if value is None:
        st.info("No data available.")
        return
    if isinstance(value, (list, tuple)):
        if not value:
            st.info("Nothing found.")
        for item in value:
            st.markdown(f"- {item}")
    elif isinstance(value, dict):
        for k, v in value.items():
            st.markdown(f"**{k}:** {v}")
    else:
        st.markdown(str(value))


def stringify_for_download(value) -> str:
    if value is None:
        return ""
    if isinstance(value, (list, tuple)):
        return "\n".join(f"- {item}" for item in value)
    if isinstance(value, dict):
        return "\n".join(f"{k}: {v}" for k, v in value.items())
    return str(value)


def reset_analysis():
    st.session_state.result = None
    st.session_state.rag_chain = None
    st.session_state.messages = []
    st.session_state.analysis_completed = False
    st.session_state.last_error = None


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown("### 🎬 AI Meeting Assistant")
    st.caption("Turn meetings into searchable knowledge.")
    st.markdown("---")

    st.session_state.active_page = st.radio(
        "Navigation",
        ["🏠 Dashboard", "📊 Meeting Analysis", "💬 Ask Meeting", "📄 Transcript"],
        index=["🏠 Dashboard", "📊 Meeting Analysis", "💬 Ask Meeting", "📄 Transcript"].index(
            st.session_state.active_page
        ),
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown("#### 🌐 Language")
    st.session_state.language = st.selectbox(
        "Language",
        ["english", "hinglish"],
        format_func=lambda x: "English" if x == "english" else "Hinglish",
        label_visibility="collapsed",
    )

    st.markdown("#### 🎥 Source")
    input_type = st.radio(
        "Input type",
        ["YouTube URL", "Local File"],
        label_visibility="collapsed",
    )

    source_value = None

    if input_type == "YouTube URL":
        source_value = st.text_input(
            "YouTube URL",
            placeholder="Paste YouTube meeting URL",
            label_visibility="collapsed",
        )
    else:
        uploaded_file = st.file_uploader(
            "Upload meeting file",
            type=["mp3", "wav", "m4a", "mp4", "webm"],
            label_visibility="collapsed",
        )
        if uploaded_file is not None:
            # Persist upload to disk so the existing backend (which expects a
            # path / source string) can consume it without any modification.
            import os

            os.makedirs("downloades", exist_ok=True)
            save_path = os.path.join("downloades", uploaded_file.name)
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            source_value = save_path
            st.success(f"Uploaded: {uploaded_file.name}")

    st.markdown("---")
    analyze_clicked = st.button("🚀 Analyze Meeting", use_container_width=True)

    if st.session_state.analysis_completed:
        st.markdown("---")
        st.markdown(
            '<span class="badge-pill">🟢 Analysis Complete</span>',
            unsafe_allow_html=True,
        )


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
<div class="app-header">
    <div>
        <p class="title">🎬 AI Meeting Assistant</p>
        <p class="subtitle">Transcribe. Understand. Search.</p>
        <p class="tech-badges">Whisper • Mistral • ChromaDB • RAG</p>
    </div>
    <div><span class="badge-pill">● AI Powered</span></div>
</div>
""",
    unsafe_allow_html=True,
)


# ============================================================
# ANALYSIS TRIGGER
# ============================================================

if analyze_clicked:
    if not source_value:
        st.error("❌ Please provide a YouTube URL or upload a file before analyzing.")
    else:
        reset_analysis()
        st.session_state.source = source_value

        try:
            stages = [
                "🎧 Processing audio...",
                "🎙️ Transcribing meeting...",
                "🏷️ Generating meeting title...",
                "📝 Generating summary...",
                "📌 Extracting action items...",
                "🔑 Extracting key decisions...",
                "❓ Extracting open questions...",
                "🧠 Building RAG knowledge base...",
            ]

            with st.status("🤖 Analyzing meeting...", expanded=True) as status:
                for stage in stages:
                    st.write(stage)

                # The backend pipeline is a single blocking call - the stage
                # labels above communicate what it is doing internally, but
                # we cannot report real progress the backend does not expose.
                result = run_pipeline(source_value, st.session_state.language)

                st.session_state.result = result
                st.session_state.rag_chain = result.get("rag_chain")
                st.session_state.analysis_completed = True

                status.update(label="✅ Analysis complete!", state="complete", expanded=False)

            st.session_state.active_page = "📊 Meeting Analysis"
            st.rerun()

        except Exception as e:
            st.session_state.last_error = str(e)
            st.session_state.analysis_completed = False


if st.session_state.last_error:
    st.error("❌ Analysis failed")
    st.markdown(
        "Something went wrong while processing your meeting. "
        "This is usually caused by an invalid source, network issue, or a "
        "backend processing error."
    )
    if st.button("🔄 Try Again"):
        st.session_state.last_error = None
        st.rerun()


# ============================================================
# PAGE: DASHBOARD
# ============================================================

def render_dashboard():
    st.markdown("## 🎬 AI Meeting Assistant")
    st.markdown(
        "##### Transform long meetings into clear, actionable insights."
    )
    st.markdown(
        "Upload a meeting recording or paste a YouTube URL. "
        "The AI will transcribe, summarize, extract action items, "
        "identify decisions, and create a searchable meeting assistant."
    )

    st.markdown("<br>", unsafe_allow_html=True)

    cols = st.columns(4)
    features = [
        ("🎙️", "Smart Transcription", "Powered by Whisper"),
        ("📝", "AI Summary", "Powered by Mistral"),
        ("📌", "Action Items", "Automatically extracted"),
        ("💬", "Ask Anything", "RAG-powered meeting chat"),
    ]
    for col, (icon, title, sub) in zip(cols, features):
        with col:
            st.markdown(
                f"""
                <div class="feature-card">
                    <div class="icon">{icon}</div>
                    <div class="f-title">{title}</div>
                    <div class="f-sub">{sub}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    if not st.session_state.analysis_completed:
        st.markdown("<br>", unsafe_allow_html=True)
        st.info("👈 Choose a source in the sidebar and click **Analyze Meeting** to get started.")


# ============================================================
# PAGE: MEETING ANALYSIS
# ============================================================

def render_analysis():
    result = st.session_state.result

    if not result:
        st.warning("No analysis yet. Go to the Dashboard and analyze a meeting first.")
        return

    st.markdown("### 🏷️ Meeting Title")
    st.markdown(f"<div class='card'><h4>{result.get('title', 'Untitled Meeting')}</h4></div>", unsafe_allow_html=True)

    # Status row
    transcript = result.get("transcript", "") or ""
    word_count = len(transcript.split()) if isinstance(transcript, str) else 0

    status_cols = st.columns(4)
    with status_cols[0]:
        st.markdown(
            f"<div class='stat-card'><div class='stat-value'>{safe_count(result.get('action_items'))}</div>"
            f"<div class='stat-label'>📌 Action Items</div></div>",
            unsafe_allow_html=True,
        )
    with status_cols[1]:
        st.markdown(
            f"<div class='stat-card'><div class='stat-value'>{safe_count(result.get('key_decisions'))}</div>"
            f"<div class='stat-label'>🔑 Key Decisions</div></div>",
            unsafe_allow_html=True,
        )
    with status_cols[2]:
        st.markdown(
            f"<div class='stat-card'><div class='stat-value'>{safe_count(result.get('open_questions'))}</div>"
            f"<div class='stat-label'>❓ Open Questions</div></div>",
            unsafe_allow_html=True,
        )
    with status_cols[3]:
        st.markdown(
            f"<div class='stat-card'><div class='stat-value'>{word_count}</div>"
            f"<div class='stat-label'>📄 Words Transcribed</div></div>",
            unsafe_allow_html=True,
        )

    st.markdown(
        f"<p style='color:#8b8ba8; font-size:0.85rem; margin-top:0.8rem;'>"
        f"Language: <b>{st.session_state.language.capitalize()}</b> &nbsp;•&nbsp; "
        f"Source: <b>{st.session_state.source}</b></p>",
        unsafe_allow_html=True,
    )

    st.markdown("<div class='section-title'>📝 Summary</div>", unsafe_allow_html=True)
    with st.container():
        st.markdown(f"<div class='card'>{result.get('summary', '')}</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-title'>📌 Action Items</div>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        render_block(result.get("action_items"))
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-title'>🔑 Key Decisions</div>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        render_block(result.get("key_decisions"))
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-title'>❓ Open Questions</div>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        render_block(result.get("open_questions"))
        st.markdown("</div>", unsafe_allow_html=True)

    # Downloads
    st.markdown("<div class='section-title'>⬇️ Downloads</div>", unsafe_allow_html=True)
    dl_cols = st.columns(3)

    with dl_cols[0]:
        st.download_button(
            "📄 Download Transcript",
            data=stringify_for_download(transcript),
            file_name="transcript.txt",
            mime="text/plain",
            use_container_width=True,
        )
    with dl_cols[1]:
        st.download_button(
            "📝 Download Summary",
            data=stringify_for_download(result.get("summary")),
            file_name="summary.txt",
            mime="text/plain",
            use_container_width=True,
        )
    with dl_cols[2]:
        report_parts = [
            f"MEETING REPORT",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "",
            f"TITLE\n{result.get('title', '')}",
            "",
            f"SUMMARY\n{stringify_for_download(result.get('summary'))}",
            "",
            f"ACTION ITEMS\n{stringify_for_download(result.get('action_items'))}",
            "",
            f"KEY DECISIONS\n{stringify_for_download(result.get('key_decisions'))}",
            "",
            f"OPEN QUESTIONS\n{stringify_for_download(result.get('open_questions'))}",
        ]
        st.download_button(
            "📋 Download Full Report",
            data="\n".join(report_parts),
            file_name="meeting_report.txt",
            mime="text/plain",
            use_container_width=True,
        )


# ============================================================
# PAGE: TRANSCRIPT
# ============================================================

def render_transcript():
    result = st.session_state.result

    if not result:
        st.warning("No transcript yet. Go to the Dashboard and analyze a meeting first.")
        return

    transcript = result.get("transcript", "") or ""
    word_count = len(transcript.split()) if isinstance(transcript, str) else 0
    char_count = len(transcript) if isinstance(transcript, str) else 0

    st.markdown("### 📄 Meeting Transcript")
    st.markdown(
        f"<p style='color:#8b8ba8; font-size:0.85rem;'>"
        f"{word_count} words &nbsp;•&nbsp; {char_count} characters</p>",
        unsafe_allow_html=True,
    )

    st.text_area("Transcript", value=transcript, height=420, label_visibility="collapsed")

    col1, col2 = st.columns([1, 3])
    with col1:
        st.download_button(
            "📋 Copy / Download Transcript",
            data=transcript,
            file_name="transcript.txt",
            mime="text/plain",
        )


# ============================================================
# PAGE: ASK MEETING (RAG CHAT)
# ============================================================

def render_chat():
    st.markdown("### 💬 Ask Your Meeting")
    st.caption("Ask questions about what was discussed in the meeting.")

    rag_chain = st.session_state.rag_chain

    if not rag_chain:
        st.warning("No meeting analyzed yet. Analyze a meeting first to unlock chat.")
        return

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    question = st.chat_input("What were the main topics discussed?")

    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    answer = rag_chain.invoke(question)
                except Exception as e:
                    answer = f"❌ Error while answering question: {e}"
            st.markdown(answer)

        st.session_state.messages.append({"role": "assistant", "content": answer})


# ============================================================
# ROUTER
# ============================================================

page = st.session_state.active_page

if page == "🏠 Dashboard":
    render_dashboard()
elif page == "📊 Meeting Analysis":
    render_analysis()
elif page == "💬 Ask Meeting":
    render_chat()
elif page == "📄 Transcript":
    render_transcript()