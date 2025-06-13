# session_manager.py
from __future__ import annotations
from typing import Dict
from langchain.memory import ConversationBufferWindowMemory
from .database import AsyncSessionLocal
from sqlalchemy import text

class Session:
    def __init__(self, resume_text: str, metadata: dict = {}):
        self.resume_text: str = resume_text
        self.metadata: dict = metadata
        self.memory: ConversationBufferWindowMemory = new_memory()
        
    def set_metadata(self, metadata: dict):
        self.metadata = metadata


def new_memory(k: int = 2) -> ConversationBufferWindowMemory:
    """Return a sliding-window memory holding the last *k* turns."""
    return ConversationBufferWindowMemory(k=k, return_messages=True)

class SessionManager:
    """Tiny in-memory store -- production apps should use Redis/DB."""
    def __init__(self):
        self._sessions: Dict[str, Session] = {}

    # ── API ────────────────────────────────────────────────────────────────
    def create(self, resume_text: str, metadata: dict = {}) -> str:
        sid = str(len(self._sessions) + 1)
        self._sessions[sid] = Session(resume_text, metadata)
        return sid
    
    def set_metadata(self, sid: str, metadata: dict):
        self._sessions[sid].set_metadata(metadata)

    async def get(self, sid: str) -> Session:
        if sid not in self._sessions:
            # Get resume from database
            print("Getting resume from database")
            async with AsyncSessionLocal() as db:
                print("DB initialized")
                try:
                    result = await db.execute(
                        text("SELECT raw_text FROM resumes WHERE user_id = :sid"),
                        {"sid": sid}
                    )
                    resume = result.fetchone()
                    if resume is None:
                        raise KeyError(f"No resume found for user {sid!r}")
                    
                    # Create new session with resume text from DB
                    self._sessions[sid] = Session(resume.raw_text, metadata)
                except Exception as e:
                    print(f"Database error: {e}")
                    raise KeyError(f"Error fetching resume for user {sid!r}: {e}")

        return self._sessions[sid]


# singleton used by the FastAPI app
session_manager = SessionManager()
