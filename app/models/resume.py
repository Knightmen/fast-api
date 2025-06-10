from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

class ResumeBase(BaseModel):
    user_id: str = Field(..., description="User identifier")
    raw_text: str = Field(..., description="Raw text content of the resume")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata about the resume")

class ResumeCreate(ResumeBase):
    pass

class Resume(ResumeBase):
    id: int = Field(..., description="Unique resume identifier")
    created_at: datetime = Field(default_factory=datetime.now, description="Timestamp when the resume was created")
    updated_at: datetime = Field(default_factory=datetime.now, description="Timestamp when the resume was last updated")

    class Config:
        from_attributes = True 