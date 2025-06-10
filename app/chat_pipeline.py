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

# ────────────────────────────────────────────────────────────────────────────
# 2. Helpers
# ────────────────────────────────────────────────────────────────────────────
def new_memory(k: int = 0) -> ConversationBufferWindowMemory:
    """Return a sliding-window memory holding the last *k* turns."""
    return ConversationBufferWindowMemory(k=k, return_messages=True)


def _prompt_from_resume(resume_text: str) -> ChatPromptTemplate:
    """Create a prompt template that embeds *this* resume."""
    system_msg = f"""
You are a helpful assistant. **Only** use the information in the resume
below to answer. If the answer is not present, reply "Can not reply at this moment!".

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


def build_chain(resume_text: str, memory: ConversationBufferWindowMemory) -> LLMChain:
    """Return an LLMChain specific to this resume + memory."""
    prompt = _prompt_from_resume(resume_text)
    print(prompt)
    return LLMChain(llm=llm, prompt=prompt, memory=memory)


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
