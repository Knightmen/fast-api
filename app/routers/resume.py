from fastapi import APIRouter, HTTPException, Depends, Security, Query
from fastapi.security.api_key import APIKeyHeader
from typing import Optional
import os
from pathlib import Path
import requests
from PyPDF2 import PdfReader
from io import BytesIO
from ..models.resume import Resume
from datetime import datetime
from ..session_manager import session_manager

router = APIRouter(
    prefix="/resume",
    tags=["resume"]
)

# Get the API key from environment
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    print("Warning: API_KEY environment variable is not set.")
    print(f"Please create a .env file in {Path(__file__).resolve().parent.parent.parent} with API_KEY=your-secret-key")

api_key_header = APIKeyHeader(name="Authorization", auto_error=True)

async def get_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )
    return api_key

@router.get("/parse", response_model=dict)
async def parse_resume(
    fileName: str = Query(..., description="Name of the resume file to parse"),
    api_key: str = Depends(get_api_key),
):
    try:
        # Construct the S3 URL
        s3_url = f"https://bonga-resume.s3.ap-southeast-2.amazonaws.com/resumes/{fileName}"
        
        # Fetch the PDF file
        response = requests.get(s3_url)
        if response.status_code != 200:
            raise HTTPException(
                status_code=404,
                detail=f"PDF file not found at {s3_url}"
            )
        
        # Read the PDF content
        pdf_file = BytesIO(response.content)
        pdf_reader = PdfReader(pdf_file)
        
        # Metadata - FileName, FileSize, FileType
        metadata = {
            "fileName": fileName,
            "fileSize": f"{int(response.headers.get('Content-Length', 0)) / 1024:.2f} KB",
            "fileType": "pdf"
        }

        # Extract text from all pages
        text_content = ""
        for page in pdf_reader.pages:
            text_content += page.extract_text()

        session_id = session_manager.create(text_content)
        
        return {
            "status": "success",
            "fileName": fileName,
            "text_content": text_content,
            "metadata": metadata,
            "session_id": session_id
        }
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch PDF: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        ) 
    
    

