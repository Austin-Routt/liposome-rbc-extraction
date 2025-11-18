"""
Tool functions for PDF processing, text manipulation, and validation.

These tools are used by agents to perform specific tasks.
"""

from .pdf_tools import (
    extract_text_from_pdf,
    extract_text_blocks_from_pdf,
    get_pdf_metadata,
)

from .text_tools import (
    normalize_scientific_text,
    normalize_text_for_matching,
    extract_sentences,
)

from .validation_tools import (
    validate_context_quote,
    fuzzy_match_text,
)

__all__ = [
    "extract_text_from_pdf",
    "extract_text_blocks_from_pdf",
    "get_pdf_metadata",
    "normalize_scientific_text",
    "normalize_text_for_matching",
    "extract_sentences",
    "validate_context_quote",
    "fuzzy_match_text",
]
