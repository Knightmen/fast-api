"""
chat_pipeline.py  ──  Build one LLMChain per (resume_text, memory)

Functions you'll use elsewhere:
    • new_memory(k=2)           → fresh ConversationBufferWindowMemory
    • build_chain(resume, mem)  → LLMChain wired to that memory + resume
"""

from __future__ import annotations
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import LLMChain
from langsmith import traceable
from .langsmith_config import setup_langsmith_tracing
from .session_manager import Session
# Initialize LangSmith tracing
setup_langsmith_tracing()

# ────────────────────────────────────────────────────────────────────────────
# 1. Gemini model (shared, thread-safe)
# ────────────────────────────────────────────────────────────────────────────
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",          # pick any Gemini chat model
    temperature=0.8,
    max_tokens=1024,
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    convert_system_message_to_human=True,  # Convert system messages to human messages
)



def _prompt_for_metadata(resume_text: str) -> ChatPromptTemplate:
    system_msg = f"""
    There is a resume below.
    --- RESUME START ---
    {resume_text}
    --- RESUME END ---
    """.strip()
    return ChatPromptTemplate.from_messages(
        [
            ("system", system_msg),
            MessagesPlaceholder("history"),   # conversation memory
            ("human", "{question}"),          # new user message
        ]
    )


def _prompt_from_resume(resume_text: str, metadata: dict) -> ChatPromptTemplate:
    # Format metadata in a way that won't be parsed as template variables
    metadata_text = "\n".join([f"{k}: {v}" for k, v in metadata.items()])
    
    system_msg = f"""
    You are a helpful assistant. There is a resume of the user below. Use the information in the resume as a context.
    You can use the information in the resume to answer the user's question. 
    For Name, contact information, address use the metadata to answer the user's question.
    In the user's question, if the question contains words like "cover letter", "email", "application", "message" or any descriptive message,
    then you should generate a response that is concise and approximately 120 words, unless the user explicitly specifies a different length. 
    You should maintain a professional tone and use the resume information to personalize the content.
    --- RESUME START ---
    {resume_text.replace("{", "\n").replace("}", "\n")}
    --- RESUME END ---
    --- METADATA START ---
    {metadata_text.replace("{", "\n").replace("}", "\n")}
    --- METADATA END ---
    """.strip()

    print(system_msg)

    return ChatPromptTemplate.from_messages(
        [
            ("system", system_msg),
            MessagesPlaceholder("history"),   # conversation memory
            ("human", "{question}"),          # new user message
        ]
    )

def build_chain(session: Session, prompt_type: str = "chat") -> LLMChain:
    if prompt_type == "chat":
        prompt = _prompt_from_resume(session.resume_text, session.metadata)
    elif prompt_type == "metadata":
        prompt = _prompt_for_metadata(session.resume_text)
    else:
        raise ValueError(f"Invalid prompt type: {prompt_type}")
    print(prompt)
    return LLMChain(llm=llm, prompt=prompt, memory=session.memory)


@traceable(name="chat_prediction")
def predict_with_monitoring(chain: LLMChain, question: str, session_id: str = None) -> dict:
    """
    Wrapper function to make LLM predictions with LangSmith monitoring.
    
    Args:
        chain: The LLMChain to use for prediction
        question: The user's question
        session_id: Optional session identifier for tracking
        
    Returns:
        Dictionary containing the answer and metadata
    """
    try:
        # Make the prediction with the chain
        answer = chain.predict(question=question)
        return {
            "answer": answer,
            "session_id": session_id,
            "status": "success",
            "question": question
        }
    except Exception as e:
        return {
            "answer": f"Error: {str(e)}",
            "session_id": session_id,
            "status": "error",
            "question": question,
            "error": str(e)
        }

# Specify which symbols should be available when using "from chat_pipeline import *"
# Only expose the new_memory() and build_chain() functions as the public API
__all__ = ["new_memory", "build_chain", "predict_with_monitoring"]
