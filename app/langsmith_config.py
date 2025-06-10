"""
LangSmith configuration for monitoring AI/LLM usage, tokens, and resources.
"""
import os
from typing import Optional


def setup_langsmith_tracing(
    project_name: Optional[str] = None,
    api_key: Optional[str] = None,
    endpoint: Optional[str] = None
) -> None:
    """
    Configure LangSmith for monitoring and tracing.
    
    Args:
        project_name: Name of the LangSmith project (defaults to LANGCHAIN_PROJECT env var)
        api_key: LangSmith API key (defaults to LANGCHAIN_API_KEY env var)
        endpoint: LangSmith endpoint (defaults to LANGCHAIN_ENDPOINT env var)
    """
    # Set up environment variables for LangSmith
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    
    # Use provided values or fall back to environment variables
    if project_name or os.getenv("LANGCHAIN_PROJECT"):
        os.environ["LANGCHAIN_PROJECT"] = project_name or os.getenv("LANGCHAIN_PROJECT", "fastapi-chat-app")
    else:
        os.environ["LANGCHAIN_PROJECT"] = "fastapi-chat-app"
    
    if api_key or os.getenv("LANGCHAIN_API_KEY"):
        os.environ["LANGCHAIN_API_KEY"] = api_key or os.getenv("LANGCHAIN_API_KEY")
    
    if endpoint or os.getenv("LANGCHAIN_ENDPOINT"):
        os.environ["LANGCHAIN_ENDPOINT"] = endpoint or os.getenv("LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com")
    else:
        os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"


def get_langsmith_status() -> dict:
    """
    Get the current LangSmith configuration status.
    
    Returns:
        Dictionary with LangSmith configuration details
    """
    return {
        "tracing_enabled": os.getenv("LANGCHAIN_TRACING_V2") == "true",
        "project_name": os.getenv("LANGCHAIN_PROJECT"),
        "api_key_configured": bool(os.getenv("LANGCHAIN_API_KEY")),
        "endpoint": os.getenv("LANGCHAIN_ENDPOINT"),
    } 