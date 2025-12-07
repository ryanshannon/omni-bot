from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import structlog

from .config import settings
from .logging_config import configure_logging
from .models import BriefResponse
from .exceptions import OmniAgentException, DataNotFoundException

configure_logging()
logger = structlog.get_logger()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)


@app.exception_handler(DataNotFoundException)
async def data_not_found_handler(request: Request, exc: DataNotFoundException):
    """Handle DataNotFoundException with 404 response."""
    logger.warning("data_not_found", error=str(exc), path=request.url.path)
    return JSONResponse(
        status_code=404,
        content={"error": str(exc)}
    )


@app.exception_handler(OmniAgentException)
async def omniagent_exception_handler(request: Request, exc: OmniAgentException):
    """Handle OmniAgentException with 500 response."""
    logger.error("omniagent_exception", error=str(exc), path=request.url.path)
    return JSONResponse(
        status_code=500,
        content={"error": str(exc)}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions with 500 response."""
    logger.error("unhandled_exception", exc_info=exc, path=request.url.path)
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"}
    )


@app.on_event("startup")
async def startup_event():
    logger.info("application_starting", app_name=settings.app_name)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    logger.debug("health_check_called")
    return {"status": "ok"}


@app.get("/brief/latest", response_model=BriefResponse)
async def get_latest_brief() -> BriefResponse:
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

    return BriefResponse(
        content=placeholder_text.strip(),
        format="markdown",
        generated_at=None
    )
