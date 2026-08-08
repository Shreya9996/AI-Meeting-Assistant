import os

from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda

from core.vector_store import (
    build_vector_store,
    load_vector_store,
    get_retriever
)


# ─────────────────────────────────────────────
# 🤖 LLM
# ─────────────────────────────────────────────

def get_llm():

    return init_chat_model(
        "mistral-small-latest",
        mistral_api_key=os.getenv("MISTRAL_API_KEY"),
        temperature=0.3
    )


# ─────────────────────────────────────────────
# 📄 Format Retrieved Documents
# ─────────────────────────────────────────────

def format_docs(docs):

    return "\n\n".join(
        [doc.page_content for doc in docs]
    )


# ─────────────────────────────────────────────
# 🧠 Build RAG Chain
# ─────────────────────────────────────────────

def build_rag_chain(transcript: str):

    print("🔎 Building RAG vector store...")

    # Create vector database from transcript
    vector_store = build_vector_store(transcript)

    # Create retriever
    retriever = get_retriever(vector_store)

    # Load LLM
    llm = get_llm()

    # ─────────────────────────────────────────
    # 📝 Prompt
    # ─────────────────────────────────────────

    prompt = ChatPromptTemplate.from_messages([

        (
            "system",
            """
You are an expert AI meeting assistant.

Answer the user's question ONLY using the meeting transcript
content provided below.

If the answer is not found in the transcript, say:

"I could not find this information in the meeting transcript."

Be concise, accurate and clear.

Meeting transcript content:

{content}
            """
        ),

        (
            "human",
            "{question}"
        )
    ])

    # ─────────────────────────────────────────
    # 🔗 RAG CHAIN
    # ─────────────────────────────────────────

    rag_chain = (

        {
            # Retrieve relevant transcript chunks
            "content": retriever | RunnableLambda(format_docs),

            # Pass user's question directly
            "question": RunnablePassthrough()
        }

        # Send both context + question to prompt
        | prompt

        # Send prompt to Mistral
        | llm

        # Convert AIMessage → string
        | StrOutputParser()
    )

    print("✅ RAG chain ready!")

    return rag_chain


# ─────────────────────────────────────────────
# 💾 Load Existing RAG Chain
# ─────────────────────────────────────────────

def load_rag_chain():

    vector_store = load_vector_store()

    retriever = get_retriever(vector_store)

    llm = get_llm()

    prompt = ChatPromptTemplate.from_messages([

        (
            "system",
            """
You are an expert AI meeting assistant.

Answer the user's question ONLY using the meeting
transcript content provided below.

If the answer is not found, say:

"I could not find this information in the meeting transcript."

Be concise and precise.

Meeting transcript content:

{content}
            """
        ),

        (
            "human",
            "{question}"
        )
    ])

    rag_chain = (

        {
            "content": retriever | RunnableLambda(format_docs),
            "question": RunnablePassthrough()
        }

        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain


# ─────────────────────────────────────────────
# 💬 Ask Question
# ─────────────────────────────────────────────

def ask_question(rag_chain, question: str) -> str:

    print(f"\n👤 Question: {question}")

    print("🤖 AI: Thinking...")

    answer = rag_chain.invoke(question)

    print(f"\n💡 Answer:\n{answer}")

    return answer