from dotenv import load_dotenv
load_dotenv()
from utils.audio_processor import process_input
from core.transcriber import transcribe_all
from core.summarizer import genrate_title,summarize
from core.extractor import extract_questions,extract_action_items,extract_key_decisions
from core.rag_engine import build_rag_chain



# from dotenv import load_dotenv

# load_dotenv()

# from utils.audio_processor import process_input
# from core.transcriber import transcribe_all
# from core.summarizer import generate_title, summarize
# from core.extractor import (
#     extract_action_items,
#     extract_questions,
#     extracter_key_decisions
# )
# from core.rag_engine import build_rag_chain


# ============================================================
# 🚀 MAIN PIPELINE
# ============================================================

def run_pipeline(source: str, language: str = "english") -> dict:

    print("\n" + "=" * 70)
    print("🎬 AI MEETING ASSISTANT")
    print("=" * 70)

    # --------------------------------------------------------
    # STEP 1: Download / Process Audio
    # --------------------------------------------------------

    print("\n🎧 Processing audio...")

    chunks = process_input(source)

    print(f"✅ Audio ready - {len(chunks)} chunks created.")

    # --------------------------------------------------------
    # STEP 2: Transcription
    # --------------------------------------------------------

    print("\n🎙️ Transcribing meeting...")

    transcript = transcribe_all(chunks)

    print("\n📝 Transcription completed!")

    print("\n" + "-" * 70)
    print("📄 TRANSCRIPT PREVIEW")
    print("-" * 70)

    print(transcript[:2000])

    if len(transcript) > 2000:
        print("\n... [Transcript continues]")

    # --------------------------------------------------------
    # STEP 3: Generate Meeting Title
    # --------------------------------------------------------

    print("\n🏷️ Generating meeting title...")

    title = genrate_title(transcript)

    # --------------------------------------------------------
    # STEP 4: Generate Summary
    # --------------------------------------------------------

    print("📝 Generating meeting summary...")

    summary = summarize(transcript)

    # --------------------------------------------------------
    # STEP 5: Extract Action Items
    # --------------------------------------------------------

    print("📌 Extracting action items...")

    action_items = extract_action_items(transcript)

    # --------------------------------------------------------
    # STEP 6: Extract Key Decisions
    # --------------------------------------------------------

    print("🔑 Extracting key decisions...")

    decisions = extract_key_decisions(transcript)

    # --------------------------------------------------------
    # STEP 7: Extract Open Questions
    # --------------------------------------------------------

    print("❓ Extracting open questions...")

    questions = extract_questions(transcript)

    # --------------------------------------------------------
    # STEP 8: Build RAG
    # --------------------------------------------------------

    print("\n🧠 Building RAG knowledge base...")

    rag_chain = build_rag_chain(transcript)

    print("✅ RAG system ready!")

    # --------------------------------------------------------
    # RETURN RESULT
    # --------------------------------------------------------

    return {
        "title": title,
        "transcript": transcript,
        "summary": summary,
        "action_items": action_items,
        "key_decisions": decisions,
        "open_questions": questions,
        "rag_chain": rag_chain
    }


# ============================================================
# 🎨 DISPLAY RESULTS
# ============================================================

def display_results(result: dict):

    print("\n\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 18 + "🎬 MEETING ANALYSIS" + " " * 31 + "║")
    print("╚" + "═" * 68 + "╝")

    # --------------------------------------------------------
    # TITLE
    # --------------------------------------------------------

    print("\n🏷️  TITLE")
    print("-" * 70)
    print(result["title"])

    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    print("\n📝 SUMMARY")
    print("-" * 70)
    print(result["summary"])

    # --------------------------------------------------------
    # ACTION ITEMS
    # --------------------------------------------------------

    print("\n📌 ACTION ITEMS")
    print("-" * 70)
    print(result["action_items"])

    # --------------------------------------------------------
    # KEY DECISIONS
    # --------------------------------------------------------

    print("\n🔑 KEY DECISIONS")
    print("-" * 70)
    print(result["key_decisions"])

    # --------------------------------------------------------
    # OPEN QUESTIONS
    # --------------------------------------------------------

    print("\n❓ OPEN QUESTIONS")
    print("-" * 70)
    print(result["open_questions"])

    print("\n" + "=" * 70)


# ============================================================
# 💬 RAG CHAT
# ============================================================

def chat_with_meeting(rag_chain):

    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 20 + "💬 MEETING CHAT" + " " * 33 + "║")
    print("╚" + "═" * 68 + "╝")

    print("\n🤖 You can now ask questions about the meeting.")
    print("💡 Type 'exit' to stop the chat.\n")

    while True:

        question = input("👤 You: ").strip()

        # Empty question
        if not question:
            print("⚠️ Please enter a question.")
            continue

        # Exit
        if question.lower() in ["exit", "quit", "q"]:

            print("\n👋 Chat ended.")
            print("🎬 Thank you for using AI Meeting Assistant!")

            break

        try:

            print("\n🤖 AI: Thinking...\n")

            answer = rag_chain.invoke(question)

            print("🤖 AI:")
            print(answer)

            print("\n" + "-" * 70)

        except Exception as e:

            print("\n❌ Error while answering question:")
            print(e)


# ============================================================
# 🏁 MAIN ENTRY POINT
# ============================================================

if __name__ == "__main__":

    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "🎬 AI MEETING ASSISTANT" + " " * 30 + "║")
    print("║" + " " * 18 + "Powered by Whisper + Mistral + RAG" + " " * 17 + "║")
    print("╚" + "═" * 68 + "╝")

    # --------------------------------------------------------
    # INPUT SOURCE
    # --------------------------------------------------------

    source = input(
        "\n🎥 Enter YouTube URL or local file path: "
    ).strip()

    if not source:

        print("❌ No source provided.")
        exit()

    # --------------------------------------------------------
    # LANGUAGE
    # --------------------------------------------------------

    language = input(
        "🌐 Language (english/hinglish): "
    ).strip().lower()

    if not language:
        language = "english"

    if language not in ["english", "hinglish"]:

        print("⚠️ Invalid language.")
        print("Using English by default.")

        language = "english"

    # --------------------------------------------------------
    # RUN PIPELINE
    # --------------------------------------------------------

    try:

        result = run_pipeline(
            source,
            language
        )

        # ----------------------------------------------------
        # DISPLAY RESULTS
        # ----------------------------------------------------

        display_results(result)

        # ----------------------------------------------------
        # PHASE 2: RAG CHAT
        # ----------------------------------------------------

        rag_chain = result["rag_chain"]

        chat_with_meeting(rag_chain)

    except KeyboardInterrupt:

        print("\n\n🛑 Process interrupted by user.")

    except Exception as e:

        print("\n\n❌ Something went wrong!")
        print("-" * 70)
        print(e)





# def run_pipeline(sourece : str)->dict:

#     print(f"Starting AI video Assistanst ! ")

#     chunks = process_input(sourece)

#     transcript = transcribe_all(chunks)

#     print(f"Raw transcription (first 300 charcters {transcript[:2000]})")

#     title = genrate_title(transcript)

#     summary = summarize(transcript)

#     action_items = extract_action_items(transcript)

#     decision = extract_key_decisions(transcript)

#     questions = extract_questions(transcript)

#     rag_chain = build_rag_chain(transcript)

#     return {
#         "title" : title,
#         "transcript" : transcript,
#         "summary" : summary,
#         "action_items": action_items,
#         "key_decisions" : decision,
#         "open_questions" : questions,
#         "rag_chain" : rag_chain
#     }



# print(run_pipeline("https://youtu.be/VSFuqMh4hus?si=i8V3NRt1n7VoHZBE"))



