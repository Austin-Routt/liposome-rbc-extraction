"""
Text Processing Tools

Functions for normalizing, cleaning, and processing scientific text.
Handles Unicode normalization, OCR corrections, and sentence tokenization.
"""

import re
import unicodedata
from typing import List
import logging

try:
    import nltk
    from nltk.tokenize import sent_tokenize
    from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters
    NLTK_AVAILABLE = True
except ImportError:
    NLTK_AVAILABLE = False
    logging.warning("NLTK not available. Install with: pip install nltk")

logger = logging.getLogger(__name__)


def normalize_scientific_text(text: str) -> str:
    """
    Normalize scientific text for fuzzy matching.
    
    This function handles:
    - Unicode normalization
    - Special character replacement
    - OCR error corrections (subscripts, superscripts)
    - Whitespace normalization
    - Chemical notation standardization
    
    Args:
        text: Raw text to normalize
        
    Returns:
        Normalized text
    """
    if not text:
        return ""
    
    # Unicode normalization (decompose then recompose)
    text = unicodedata.normalize('NFKD', text)
    
    # Replace various dash types with standard hyphen
    text = text.replace('–', '-').replace('—', '-')
    
    # Replace curly quotes with straight quotes
    text = text.replace('"', '"').replace('"', '"')
    text = text.replace(''', "'").replace(''', "'")
    
    # OCR error corrections for superscripts/subscripts
    text = text.replace('²', '2').replace('³', '3')
    text = text.replace('¹', '1').replace('⁴', '4')
    
    # Normalize chemical isotope notation
    text = re.sub(r'\[³H\]', r'[3H]', text)
    text = re.sub(r'\[¹²⁵I\]', r'[125I]', text)
    text = re.sub(r'\[¹⁴C\]', r'[14C]', text)
    
    # Normalize whitespace (replace multiple spaces/newlines with single space)
    text = re.sub(r'\s+', ' ', text)
    
    # Remove soft hyphens
    text = text.replace('\u00ad', '')
    
    return text.strip()


def normalize_text_for_matching(text: str) -> str:
    """
    Normalize text specifically for fuzzy matching.
    
    Applies scientific normalization and converts to lowercase.
    
    Args:
        text: Text to normalize
        
    Returns:
        Normalized text ready for matching
    """
    text = normalize_scientific_text(text)
    return text.lower()


def extract_sentences(text: str) -> List[str]:
    """
    Extract sentences from text using NLTK sentence tokenizer.
    
    Configured for scientific text with common abbreviations.
    
    Args:
        text: Text to tokenize
        
    Returns:
        List of sentences
    """
    if not NLTK_AVAILABLE:
        # Fallback to simple split on periods
        logger.warning("NLTK not available, using simple sentence splitting")
        sentences = text.split('. ')
        return [s.strip() + '.' for s in sentences if s.strip()]
    
    try:
        # Configure Punkt tokenizer with scientific abbreviations
        punkt_param = PunktParameters()
        punkt_param.abbrev_types = set([
            'et', 'al', 'i.e', 'e.g', 'vs', 'Fig', 'fig', 'Dr', 'Mr', 'Mrs',
            'etc', 'cf', 'ref', 'refs', 'vol', 'p', 'pp', 'ch'
        ])
        tokenizer = PunktSentenceTokenizer(punkt_param)
        
        # Tokenize
        raw_sentences = tokenizer.tokenize(text)
        
        # Normalize each sentence
        sentences = [normalize_scientific_text(s) for s in raw_sentences if s.strip()]
        
        return sentences
        
    except Exception as e:
        logger.error(f"Error in sentence tokenization: {e}")
        # Fallback
        sentences = text.split('. ')
        return [s.strip() + '.' for s in sentences if s.strip()]


def clean_text(text: str) -> str:
    """
    General text cleaning for display and processing.
    
    Args:
        text: Text to clean
        
    Returns:
        Cleaned text
    """
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove control characters
    text = ''.join(char for char in text if unicodedata.category(char)[0] != 'C' or char in '\n\t')
    
    # Strip leading/trailing whitespace
    text = text.strip()
    
    return text


def truncate_text(text: str, max_length: int = 500, ellipsis: str = "...") -> str:
    """
    Truncate text to maximum length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        ellipsis: String to append if truncated
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(ellipsis)] + ellipsis


def extract_numbers_from_text(text: str) -> List[float]:
    """
    Extract numerical values from text.
    
    Args:
        text: Text containing numbers
        
    Returns:
        List of extracted numbers
    """
    # Pattern for numbers (including decimals, negatives, scientific notation)
    pattern = r'-?\d+\.?\d*(?:[eE][+-]?\d+)?'
    matches = re.findall(pattern, text)
    
    numbers = []
    for match in matches:
        try:
            numbers.append(float(match))
        except ValueError:
            continue
    
    return numbers


def extract_percentages(text: str) -> List[float]:
    """
    Extract percentage values from text.
    
    Args:
        text: Text containing percentages
        
    Returns:
        List of percentage values (as floats)
    """
    # Pattern for percentages
    pattern = r'(\d+\.?\d*)\s*%'
    matches = re.findall(pattern, text)
    
    percentages = []
    for match in matches:
        try:
            percentages.append(float(match))
        except ValueError:
            continue
    
    return percentages


def highlight_match(text: str, match_text: str, marker: str = "**") -> str:
    """
    Highlight matching text within a larger text string.
    
    Args:
        text: Full text
        match_text: Text to highlight
        marker: Marker to use for highlighting (default: markdown bold)
        
    Returns:
        Text with highlighted match
    """
    # Case-insensitive search
    pattern = re.compile(re.escape(match_text), re.IGNORECASE)
    return pattern.sub(f"{marker}\\g<0>{marker}", text)


def extract_units(text: str) -> List[str]:
    """
    Extract measurement units from text.
    
    Args:
        text: Text containing units
        
    Returns:
        List of identified units
    """
    common_units = [
        'nm', 'μm', 'mm', 'cm', 'm', 'km',
        'mg', 'g', 'kg',
        'ml', 'μl', 'l',
        'mol', 'mmol', 'μmol', 'nmol',
        'M', 'mM', 'μM', 'nM',
        's', 'min', 'h', 'hr',
        '°C', 'K',
        'V', 'mV',
        'Pa', 'kPa', 'MPa',
        'rpm', 'g-force',
        '%', 'mol%', 'w/v', 'v/v', 'w/w'
    ]
    
    found_units = []
    for unit in common_units:
        if unit in text:
            found_units.append(unit)
    
    return list(set(found_units))  # Remove duplicates


def ensure_nltk_data():
    """
    Ensure NLTK data is downloaded for sentence tokenization.
    """
    if not NLTK_AVAILABLE:
        return False
    
    try:
        nltk.data.find('tokenizers/punkt')
        return True
    except LookupError:
        logger.info("Downloading NLTK punkt tokenizer data...")
        try:
            nltk.download('punkt', quiet=True)
            return True
        except Exception as e:
            logger.error(f"Failed to download NLTK data: {e}")
            return False


# Initialize NLTK data on module import
if NLTK_AVAILABLE:
    ensure_nltk_data()


if __name__ == "__main__":
    # Test normalization
    test_text = "The liposome size was 150 nm ± 10 nm at 37°C. [³H]-labeled phospholipids showed..."
    print("Original:", test_text)
    print("Normalized:", normalize_scientific_text(test_text))
    print("For matching:", normalize_text_for_matching(test_text))
    
    # Test sentence extraction
    test_paragraph = "This is the first sentence. This is the second sentence with Dr. Smith et al. The third sentence follows."
    print("\nSentences:", extract_sentences(test_paragraph))
    
    # Test number extraction
    print("\nNumbers:", extract_numbers_from_text("Values were 1.5, 2.3, and 4.7 mg/ml."))
    print("Percentages:", extract_percentages("Efficiency was 85.5% and recovery was 92%."))
