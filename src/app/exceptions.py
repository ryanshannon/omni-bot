"""Custom exception classes for OmniAgent."""


class OmniAgentException(Exception):
    """Base exception for OmniAgent."""
    pass


class DataNotFoundException(OmniAgentException):
    """Raised when requested data is not found."""
    pass


class DatabaseException(OmniAgentException):
    """Raised when database operations fail."""
    pass


class IngestionException(OmniAgentException):
    """Raised when data ingestion fails."""
    pass
