"""
PDF Processing Tools

Functions for extracting text, structure, and metadata from scientific PDFs.
Based on PyMuPDF (fitz) with support for complex layouts and scientific content.
"""

import fitz  # PyMuPDF
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)


def extract_text_from_pdf(pdf_path: str) -> Dict[str, Any]:
    """
    Extract text from a PDF file.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Dictionary containing:
            - full_text: Complete text from all pages
            - page_texts: List of text from each page
            - metadata: PDF metadata
            - page_count: Number of pages
    """
    try:
        pdf_path = Path(pdf_path)
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")
        
        doc = fitz.open(str(pdf_path))
        
        page_texts = []
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text = page.get_text()
            page_texts.append(text)
        
        full_text = "\n\n".join(page_texts)
        
        metadata = {
            "title": doc.metadata.get("title", ""),
            "author": doc.metadata.get("author", ""),
            "subject": doc.metadata.get("subject", ""),
            "keywords": doc.metadata.get("keywords", ""),
            "creator": doc.metadata.get("creator", ""),
            "producer": doc.metadata.get("producer", ""),
        }
        
        doc.close()
        
        return {
            "full_text": full_text,
            "page_texts": page_texts,
            "metadata": metadata,
            "page_count": len(page_texts),
            "file_path": str(pdf_path),
        }
        
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {e}")
        raise


def extract_text_blocks_from_pdf(pdf_path: str) -> Dict[str, Any]:
    """
    Extract text blocks from a PDF with detailed structure.
    
    This function preserves more structure than simple text extraction,
    useful for context validation and quote matching.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Dictionary containing:
            - full_text: Complete text
            - blocks: Dict mapping page numbers to lists of text blocks
            - metadata: PDF metadata
    """
    try:
        pdf_path = Path(pdf_path)
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")
        
        doc = fitz.open(str(pdf_path))
        
        blocks_dict = {}
        page_texts = []
        
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            page_dict = page.get_text("dict")
            blocks = []
            
            for block in page_dict["blocks"]:
                if "lines" in block:
                    block_text = ""
                    for line in block["lines"]:
                        for span in line["spans"]:
                            block_text += span["text"]
                        block_text += " "
                    if block_text.strip():
                        blocks.append(block_text.strip())
            
            blocks_dict[page_num] = blocks
            page_texts.append("\n".join(blocks))
        
        full_text = "\n\n".join(page_texts)
        
        metadata = doc.metadata
        doc.close()
        
        return {
            "full_text": full_text,
            "blocks": blocks_dict,
            "metadata": metadata,
            "page_count": len(blocks_dict),
            "file_path": str(pdf_path),
        }
        
    except Exception as e:
        logger.error(f"Error extracting blocks from PDF: {e}")
        raise


def get_pdf_metadata(pdf_path: str) -> Dict[str, str]:
    """
    Extract metadata from a PDF file.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Dictionary of metadata fields
    """
    try:
        doc = fitz.open(str(pdf_path))
        metadata = dict(doc.metadata)
        doc.close()
        return metadata
    except Exception as e:
        logger.error(f"Error extracting metadata: {e}")
        return {}


def search_text_in_pdf(
    pdf_data: Dict[str, Any],
    search_terms: List[str],
    case_sensitive: bool = False
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Search for terms in extracted PDF text.
    
    Args:
        pdf_data: Dictionary from extract_text_from_pdf or extract_text_blocks_from_pdf
        search_terms: List of terms to search for
        case_sensitive: Whether search should be case-sensitive
        
    Returns:
        Dictionary mapping search terms to list of matches with locations
    """
    results = {term: [] for term in search_terms}
    
    full_text = pdf_data.get("full_text", "")
    if not case_sensitive:
        full_text_lower = full_text.lower()
    
    for term in search_terms:
        search_term = term if case_sensitive else term.lower()
        text_to_search = full_text if case_sensitive else full_text_lower
        
        start = 0
        while True:
            pos = text_to_search.find(search_term, start)
            if pos == -1:
                break
            
            # Extract context around match
            context_start = max(0, pos - 100)
            context_end = min(len(full_text), pos + len(term) + 100)
            context = full_text[context_start:context_end]
            
            results[term].append({
                "position": pos,
                "context": context,
                "term": term
            })
            
            start = pos + 1
    
    return results


def extract_section_text(
    pdf_data: Dict[str, Any],
    section_name: str
) -> Optional[str]:
    """
    Extract text from a specific section (e.g., Methods, Results).
    
    This is a simple heuristic-based extraction. May need refinement
    for complex paper structures.
    
    Args:
        pdf_data: Dictionary from extract_text_from_pdf
        section_name: Name of section to extract (e.g., "Methods", "Results")
        
    Returns:
        Extracted section text or None if not found
    """
    full_text = pdf_data.get("full_text", "")
    
    # Common section headers
    section_patterns = {
        "abstract": ["abstract"],
        "introduction": ["introduction"],
        "methods": ["methods", "materials and methods", "experimental"],
        "results": ["results"],
        "discussion": ["discussion"],
        "conclusion": ["conclusion", "conclusions"],
        "references": ["references", "bibliography"],
    }
    
    section_key = section_name.lower()
    if section_key not in section_patterns:
        logger.warning(f"Unknown section: {section_name}")
        return None
    
    patterns = section_patterns[section_key]
    
    # Try to find section boundaries
    # This is a simplified approach
    for pattern in patterns:
        # Case-insensitive search
        import re
        matches = list(re.finditer(
            rf'\b{pattern}\b',
            full_text,
            re.IGNORECASE
        ))
        
        if matches:
            # Take the first match as section start
            start = matches[0].start()
            
            # Try to find next section
            end = len(full_text)
            for next_section_patterns in section_patterns.values():
                for next_pattern in next_section_patterns:
                    next_matches = list(re.finditer(
                        rf'\b{next_pattern}\b',
                        full_text[start + len(pattern):],
                        re.IGNORECASE
                    ))
                    if next_matches:
                        potential_end = start + len(pattern) + next_matches[0].start()
                        if potential_end > start and potential_end < end:
                            end = potential_end
            
            return full_text[start:end]
    
    return None


if __name__ == "__main__":
    # Example usage
    print("PDF Tools module loaded successfully")
    print("Available functions:")
    print("  - extract_text_from_pdf")
    print("  - extract_text_blocks_from_pdf")
    print("  - get_pdf_metadata")
    print("  - search_text_in_pdf")
    print("  - extract_section_text")
