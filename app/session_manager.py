# session_manager.py
from __future__ import annotations
from uuid import uuid4
from typing import Dict
from langchain.memory import ConversationBufferWindowMemory
from .chat_pipeline import new_memory


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

    def get(self, sid: str) -> _Session:
        if sid not in self._sessions:
            raise KeyError(f"Session {sid!r} not found.")
        return self._sessions[sid]


# singleton used by the FastAPI app
session_manager = SessionManager()
