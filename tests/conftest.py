import pytest


@pytest.fixture(autouse=True)
def reset_logging():
    """Reset logging configuration before each test."""
    import structlog

    structlog.reset_defaults()
