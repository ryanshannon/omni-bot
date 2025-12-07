from fastapi import FastAPI
from fastapi.responses import JSONResponse
import structlog

from .config import settings
from .logging_config import configure_logging

configure_logging()
logger = structlog.get_logger()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)


@app.on_event("startup")
async def startup_event():
    logger.info("application_starting", app_name=settings.app_name)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    logger.debug("health_check_called")
    return {"status": "ok"}


@app.get("/brief/latest")
async def get_latest_brief():
    """Get the latest research brief."""
    logger.info("brief_requested")

    # Phase 0: Placeholder response
    placeholder_text = """
# AI Research Brief - Placeholder

Welcome to OmniAgent! This is a placeholder brief.

## Coming Soon
- Arxiv paper aggregation
- AI-generated summaries
- Multi-source research tracking

Stay tuned for updates!
"""

    return JSONResponse(
        content={
            "content": placeholder_text.strip(),
            "format": "markdown",
            "generated_at": None,
        }
    )
