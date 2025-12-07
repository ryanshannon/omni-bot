"""API response models."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class BriefResponse(BaseModel):
    """Response model for the brief endpoint."""

    content: str
    format: str
    generated_at: Optional[datetime] = None
