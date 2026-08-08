import os

from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda


# ============================================================
# 🤖 LLM
# ============================================================

def get_llm():

    return init_chat_model(
        "mistral-small-latest",
        mistral_api_key=os.getenv("MISTRAL_API_KEY"),
        temperature=0.3
    )


# ============================================================
# 🔗 COMMON CHAIN BUILDER
# ============================================================

def build_chain(system_prompt: str):

    llm = get_llm()

    return (
        RunnablePassthrough()
        | RunnableLambda(lambda x: {"text": x})
        | ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{text}")
        ])
        | llm
        | StrOutputParser()
    )


# ============================================================
# 📌 ACTION ITEMS
# ============================================================

def extract_action_items(transcript: str) -> str:

    chain = build_chain(
        """
        You are an expert meeting analyst.

        From the meeting transcript, extract all action items.

        For each action item provide:

        - Task description
        - Deadline

        If a deadline is not mentioned, write:
        "Not specified"

        Format the result as a numbered list.

        If no action items are found, say:
        "No action items found."
        """
    )

    return chain.invoke(transcript)


# ============================================================
# ✅ KEY DECISIONS
# ============================================================

def extract_key_decisions(transcript: str) -> str:

    chain = build_chain(
        """
        You are an expert meeting analyst.

        From the meeting transcript, extract all important
        decisions that were made during the meeting.

        Format the result as a numbered list.

        If no key decisions are found, say:
        "No key decisions found."
        """
    )

    return chain.invoke(transcript)


# ============================================================
# ❓ OPEN QUESTIONS
# ============================================================

def extract_questions(transcript: str) -> str:

    chain = build_chain(
        """
        You are an expert meeting analyst.

        From the meeting transcript, extract all unresolved
        questions or topics that need follow-up.

        Format the result as a numbered list.

        If no open questions are found, say:
        "No open questions found."
        """
    )

    return chain.invoke(transcript)