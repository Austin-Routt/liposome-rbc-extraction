"""
Literature Review Automation System

A multi-agent system for automated extraction of structured information
from scientific PDFs for PRISMA scoping reviews.
"""

__version__ = "0.1.0"
__author__ = "Your Name"

from .utils.config import (
    MODEL_CONFIG,
    VALIDATION_CONFIG,
    get_agent_config,
    get_model_config,
)

__all__ = [
    "MODEL_CONFIG",
    "VALIDATION_CONFIG",
    "get_agent_config",
    "get_model_config",
]
