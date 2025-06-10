from fastapi import UploadFile, File, HTTPException, APIRouter
from pydantic import BaseModel

from ..session_manager import session_manager
from ..chat_pipeline import build_chain, predict_with_monitoring

router = APIRouter(
    prefix="/session",
    tags=["session"]
)

# ── 1️⃣  INITIALISE SESSION ───────────────────────────────────────────────
class InitRequest(BaseModel):
    resume_text: str | None = None   # optional if user uploads PDF

class InitResponse(BaseModel):
    session_id: str

@router.get("/list")
async def list_sessions():
    """List all available session IDs for debugging"""
    return {
        "available_sessions": list(session_manager._sessions.keys()),
        "total_sessions": len(session_manager._sessions)
    }


@router.post("/init", response_model=InitResponse)
async def init_session(
    resume_text: str
):
    session_id = session_manager.create(resume_text)
    return InitResponse(session_id=session_id)


# ── 2️⃣  CONVERSE ─────────────────────────────────────────────────────────
class ChatRequest(BaseModel):
    session_id: str
    message: str

class ChatResponse(BaseModel):
    answer: str
    session_id: str
    status: str

@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    try:
        session = await session_manager.get(req.session_id)
    except KeyError:
        print(f"Session {req.session_id} not found. Available sessions: {list(session_manager._sessions.keys())}")
        raise HTTPException(404, "Invalid session_id")
    
    try:
      # Build a chain *for this call* using session-specific resume + memory
      chain = build_chain(session.resume_text, session.memory)
    except Exception as e:
        print(f"Error building chain: {e}")
        raise HTTPException(500, "Error building chain")

    # Use the monitored prediction function
    result = predict_with_monitoring(chain, req.message, req.session_id)
    return ChatResponse(
        answer=result["answer"],
        session_id=result["session_id"],
        status=result["status"]
    )
