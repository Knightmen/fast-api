# session_manager.py
from __future__ import annotations
from typing import Dict
from langchain.memory import ConversationBufferWindowMemory
from .chat_pipeline import new_memory
from .database import AsyncSessionLocal
from sqlalchemy import text

class _Session:
    def __init__(self, resume_text: str):
        self.resume_text: str = resume_text
        self.memory: ConversationBufferWindowMemory = new_memory()


class SessionManager:
    """Tiny in-memory store -- production apps should use Redis/DB."""
    def __init__(self):
        self._sessions: Dict[str, _Session] = {}

    # ── API ────────────────────────────────────────────────────────────────
    def create(self, resume_text: str) -> str:
        sid = str(len(self._sessions) + 1)
        self._sessions[sid] = _Session(resume_text)
        return sid
    async def get(self, sid: str) -> _Session:
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
                    self._sessions[sid] = _Session(resume.raw_text)
                except Exception as e:
                    print(f"Database error: {e}")
                    raise KeyError(f"Error fetching resume for user {sid!r}: {e}")

        return self._sessions[sid]


# singleton used by the FastAPI app
session_manager = SessionManager()
