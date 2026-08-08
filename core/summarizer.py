from langchain.chat_models import init_chat_model 
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnableLambda,RunnablePassthrough
import os


def get_llm():
    return init_chat_model("mistral-small-latest",mistral_api_key = os.getenv("MISTRAL_API_KEY"),temperature=0.3)


def split_transcript(transcript:str)->list:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 3000,
        chunk_overlap = 200
    )

    return splitter.split_text(transcript)

def summarize(transcript:str)->str:
    llm = get_llm()

    map_prompt = ChatPromptTemplate.from_messages([
        ("system","summarizer this poration of a meeting transcript"),
        ("human","{text}")

    ])

    map_chain = map_prompt | llm | StrOutputParser()

    chunks = split_transcript(transcript)

    chunk_summaries = [map_chain.invoke({"text":chunk}) for chunk in chunks]

    combined = "\n\n".join(chunk_summaries)

    combined_prompt = ChatPromptTemplate.from_messages([
        ("system",""" you are an expert meeting summarizer combine these partial summarie  into 
                      one final professional meeting summary in bullet points. """),
        ("human","{text}")
    ])

    combined_chain = (
        combined_prompt | llm | StrOutputParser()
    )

    return combined_chain.invoke({"text" :combined})


def genrate_title(transcript : str)->str:

    llm = get_llm()

    title_chain = (
        ChatPromptTemplate.from_messages([
            ("system","""  Based on the meeting transcript , genrate a short professional meeting title 
              (max 8 words) . only return the title , nothing else. """),
            ("human","{text}")
        ]) 
         | llm | StrOutputParser()
    )


    return title_chain.invoke({"text" : transcript[:2000]})


