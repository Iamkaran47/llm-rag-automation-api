# src/api/models.py
"""Pydantic models for API requests and responses."""

from pydantic import BaseModel
from typing import Optional, Dict

class ExecuteRequest(BaseModel):
    """Model for the /execute endpoint request payload."""
    prompt: str
    session_id: Optional[str] = "default"  # Optional, defaults to "default" for context
    params: Optional[Dict[str, str]] = None  # Optional parameters for functions like run_shell_command

class ExecuteResponse(BaseModel):
    """Model for the /execute endpoint response payload."""
    function: str
    code: str