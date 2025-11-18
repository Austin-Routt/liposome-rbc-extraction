"""
Validation Tools

Functions for validating extracted data against source PDFs and schemas.
Includes fuzzy matching for context quote validation.
"""

from typing import Dict, Any, Tuple
import logging

try:
    from fuzzywuzzy import fuzz
    FUZZYWUZZY_AVAILABLE = True
except ImportError:
    FUZZYWUZZY_AVAILABLE = False
    logging.warning("fuzzywuzzy not available. Install with: pip install fuzzywuzzy python-Levenshtein")

from .text_tools import normalize_text_for_matching

logger = logging.getLogger(__name__)


def fuzzy_match_text(text1: str, text2: str, method: str = "token_sort") -> int:
    """
    Calculate fuzzy match score between two texts.
    
    Args:
        text1: First text
        text2: Second text
        method: Matching method - "ratio", "partial", "token_sort", or "token_set"
        
    Returns:
        Match score (0-100)
    """
    if not FUZZYWUZZY_AVAILABLE:
        # Fallback to exact match
        return 100 if text1 == text2 else 0
    
    # Normalize texts
    norm_text1 = normalize_text_for_matching(text1)
    norm_text2 = normalize_text_for_matching(text2)
    
    if method == "ratio":
        return fuzz.ratio(norm_text1, norm_text2)
    elif method == "partial":
        return fuzz.partial_ratio(norm_text1, norm_text2)
    elif method == "token_sort":
        return fuzz.token_sort_ratio(norm_text1, norm_text2)
    elif method == "token_set":
        return fuzz.token_set_ratio(norm_text1, norm_text2)
    else:
        raise ValueError(f"Unknown method: {method}")


def find_best_match(
    query: str,
    candidates: list,
    threshold: float = 0.90
) -> Tuple[str, float, int]:
    """
    Find the best matching candidate for a query.
    
    Args:
        query: Query string to match
        candidates: List of candidate strings
        threshold: Minimum score threshold (0-1)
        
    Returns:
        Tuple of (best_match, score, index) or ("", 0, -1) if no match
    """
    if not candidates:
        return "", 0.0, -1
    
    best_match = ""
    best_score = 0
    best_index = -1
    
    for i, candidate in enumerate(candidates):
        # Try multiple scoring methods and take the maximum
        scores = [
            fuzzy_match_text(query, candidate, "ratio"),
            fuzzy_match_text(query, candidate, "token_sort"),
            fuzzy_match_text(query, candidate, "token_set"),
            fuzzy_match_text(query, candidate, "partial"),
        ]
        score = max(scores) / 100.0  # Convert to 0-1 scale
        
        if score > best_score:
            best_score = score
            best_match = candidate
            best_index = i
    
    if best_score >= threshold:
        return best_match, best_score, best_index
    else:
        return "", 0.0, -1


def validate_context_quote(
    quote: str,
    pdf_text: str,
    threshold: float = 0.90,
    window_size: int = 300
) -> Dict[str, Any]:
    """
    Validate that a quote appears in the PDF text with sufficient similarity.
    
    Args:
        quote: Quote to validate
        pdf_text: Full PDF text or relevant section
        threshold: Similarity threshold (0-1)
        window_size: Size of text window for sliding window search
        
    Returns:
        Dictionary with validation results:
            - valid: Boolean indicating if quote was found
            - score: Best match score
            - match: Best matching text from PDF
            - position: Position in PDF text (-1 if not found)
            - method: Matching method used
    """
    if not quote.strip():
        return {
            "valid": False,
            "score": 0.0,
            "match": "",
            "position": -1,
            "method": "none",
            "error": "Empty quote"
        }
    
    # Normalize texts
    norm_quote = normalize_text_for_matching(quote)
    norm_pdf = normalize_text_for_matching(pdf_text)
    
    # Method 1: Direct exact match
    if norm_quote in norm_pdf:
        pos = norm_pdf.find(norm_quote)
        return {
            "valid": True,
            "score": 1.0,
            "match": pdf_text[pos:pos + len(quote)],
            "position": pos,
            "method": "exact_match"
        }
    
    # Method 2: High-similarity partial match
    partial_score = fuzzy_match_text(quote, pdf_text, "partial") / 100.0
    if partial_score > 0.95:
        # Try to find approximate position
        words = norm_quote.split()
        if len(words) > 3:
            # Search for first few words
            search_phrase = " ".join(words[:3])
            if search_phrase in norm_pdf:
                pos = norm_pdf.find(search_phrase)
                match_end = min(len(pdf_text), pos + len(quote) + 50)
                return {
                    "valid": True,
                    "score": partial_score,
                    "match": pdf_text[pos:match_end],
                    "position": pos,
                    "method": "partial_match"
                }
    
    # Method 3: Sliding window search
    stride = window_size // 2
    windows = []
    
    for i in range(0, max(1, len(pdf_text) - window_size + 1), stride):
        window = pdf_text[i:i + window_size]
        windows.append((window, i))
    
    # Add final window if needed
    if len(pdf_text) >= window_size:
        windows.append((pdf_text[-window_size:], len(pdf_text) - window_size))
    elif len(pdf_text) < window_size:
        windows = [(pdf_text, 0)]
    
    best_window = ""
    best_score = 0.0
    best_position = -1
    
    for window, position in windows:
        score = fuzzy_match_text(quote, window, "token_sort") / 100.0
        if score > best_score:
            best_score = score
            best_window = window
            best_position = position
    
    is_valid = best_score >= threshold
    
    return {
        "valid": is_valid,
        "score": best_score,
        "match": best_window if is_valid else "",
        "position": best_position if is_valid else -1,
        "method": "window_match" if is_valid else "no_match"
    }


def validate_json_schema(data: Dict[str, Any], schema: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate JSON data against a schema.
    
    Args:
        data: JSON data to validate
        schema: JSON schema
        
    Returns:
        Validation result with errors
    """
    try:
        import jsonschema
        from jsonschema import validate
        
        try:
            validate(instance=data, schema=schema)
            return {
                "valid": True,
                "errors": []
            }
        except jsonschema.exceptions.ValidationError as e:
            return {
                "valid": False,
                "errors": [str(e)]
            }
    except ImportError:
        logger.warning("jsonschema not available. Install with: pip install jsonschema")
        return {
            "valid": True,  # Can't validate without jsonschema
            "errors": [],
            "warning": "jsonschema not installed"
        }


def check_required_fields(data: Dict[str, Any], required_fields: list) -> Dict[str, Any]:
    """
    Check if all required fields are present in data.
    
    Args:
        data: Data dictionary
        required_fields: List of required field names
        
    Returns:
        Validation result
    """
    missing_fields = []
    
    for field in required_fields:
        if field not in data:
            missing_fields.append(field)
    
    return {
        "valid": len(missing_fields) == 0,
        "missing_fields": missing_fields,
        "present_fields": [f for f in required_fields if f in data]
    }


def calculate_match_confidence(
    matches: list,
    total_items: int,
    threshold: float = 0.90
) -> Dict[str, Any]:
    """
    Calculate overall confidence score based on match results.
    
    Args:
        matches: List of match scores (0-1)
        total_items: Total number of items
        threshold: Threshold for considering a match valid
        
    Returns:
        Confidence metrics
    """
    if total_items == 0:
        return {
            "confidence": 0.0,
            "valid_matches": 0,
            "invalid_matches": 0,
            "average_score": 0.0
        }
    
    valid_matches = sum(1 for score in matches if score >= threshold)
    invalid_matches = total_items - valid_matches
    average_score = sum(matches) / len(matches) if matches else 0.0
    
    confidence = valid_matches / total_items
    
    return {
        "confidence": confidence,
        "valid_matches": valid_matches,
        "invalid_matches": invalid_matches,
        "average_score": average_score,
        "total_items": total_items
    }


if __name__ == "__main__":
    # Test fuzzy matching
    text1 = "The liposome size was measured to be 150 nm"
    text2 = "Liposome size measured: 150nm"
    
    print("Fuzzy match scores:")
    print(f"  Ratio: {fuzzy_match_text(text1, text2, 'ratio')}")
    print(f"  Token sort: {fuzzy_match_text(text1, text2, 'token_sort')}")
    print(f"  Token set: {fuzzy_match_text(text1, text2, 'token_set')}")
    
    # Test quote validation
    quote = "The results showed significant improvement"
    pdf_text = "In our study, the results showed significant improvement in membrane stability."
    result = validate_context_quote(quote, pdf_text)
    print(f"\nQuote validation: {result}")
