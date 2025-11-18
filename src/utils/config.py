"""
Configuration settings for the Literature Review Automation System.

This module contains all configuration parameters for agents, models,
validation thresholds, and processing options.
"""

import os
from pathlib import Path
from typing import Dict, Any

# Project Paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
SCHEMAS_DIR = DATA_DIR / "schemas"
SAMPLE_PDFS_DIR = DATA_DIR / "sample_pdfs"
OUTPUTS_DIR = DATA_DIR / "outputs"
VALIDATION_REPORTS_DIR = DATA_DIR / "validation_reports"

# Ensure directories exist
for dir_path in [DATA_DIR, SCHEMAS_DIR, SAMPLE_PDFS_DIR, OUTPUTS_DIR, VALIDATION_REPORTS_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# Model Configuration
MODEL_CONFIG = {
    "model_name": "gemini-2.5-flash-lite",
    "temperature": 0.1,  # Low temperature for factual extraction
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
}

# API Configuration
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    print("⚠️  Warning: GOOGLE_API_KEY not set. Please set it in your environment.")

# Agent-Specific Settings
AGENT_CONFIGS = {
    "preprocessing": {
        "timeout_seconds": 120,
        "max_retries": 2,
        "ocr_fallback": True,
    },
    "gap_extraction": {
        "timeout_seconds": 180,
        "max_retries": 3,
        "min_gaps_expected": 1,
        "significance_threshold": "Low",  # Minimum significance to include
    },
    "variable_extraction": {
        "timeout_seconds": 180,
        "max_retries": 3,
        "min_variables_expected": 3,
    },
    "technique_extraction": {
        "timeout_seconds": 180,
        "max_retries": 3,
        "min_techniques_expected": 4,
    },
    "finding_extraction": {
        "timeout_seconds": 180,
        "max_retries": 3,
        "min_findings_expected": 2,
    },
    "assessment": {
        "timeout_seconds": 120,
        "max_retries": 2,
    },
    "validation": {
        "timeout_seconds": 60,
        "max_retries": 1,
    },
}

# Validation Thresholds
VALIDATION_CONFIG = {
    "context_match_threshold": 0.90,  # 90% similarity for quote validation
    "max_validation_retries": 3,
    "schema_strict": True,  # Strict schema validation
    "required_fields_check": True,
}

# PDF Processing Settings
PDF_PROCESSING_CONFIG = {
    "extract_images": False,
    "extract_tables": True,
    "dpi": 300,
    "normalize_unicode": True,
    "preserve_formatting": False,
}

# Orchestration Settings
ORCHESTRATION_CONFIG = {
    "parallel_extraction": True,  # Run extraction agents in parallel
    "max_concurrent_agents": 4,
    "checkpoint_enabled": True,  # Save progress at checkpoints
    "human_review_threshold": 0.75,  # Confidence below this flags for review
}

# Logging Configuration
LOGGING_CONFIG = {
    "level": "INFO",  # DEBUG, INFO, WARNING, ERROR
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": PROJECT_ROOT / "logs" / "processing.log",
    "console": True,
}

# Schema File Path
SCHEMA_FILE = SCHEMAS_DIR / "fulltext_screening_schema.json"

# Output Settings
OUTPUT_CONFIG = {
    "indent": 2,  # JSON indentation
    "sort_keys": False,
    "ensure_ascii": False,
    "save_intermediate": True,  # Save outputs from each agent
    "generate_reports": True,
}

# Cost Tracking (for monitoring)
COST_CONFIG = {
    "track_costs": True,
    "gemini_flash_lite_input_cost": 0.0,  # Free tier
    "gemini_flash_lite_output_cost": 0.0,  # Free tier
    "budget_limit": None,  # No limit for free tier
}


def get_agent_config(agent_name: str) -> Dict[str, Any]:
    """Get configuration for a specific agent."""
    return AGENT_CONFIGS.get(agent_name, {})


def get_model_config() -> Dict[str, Any]:
    """Get model configuration."""
    return MODEL_CONFIG.copy()


def get_validation_config() -> Dict[str, Any]:
    """Get validation configuration."""
    return VALIDATION_CONFIG.copy()


def validate_setup() -> bool:
    """Validate that all required setup is complete."""
    checks = {
        "API Key Set": API_KEY is not None,
        "Schema File Exists": SCHEMA_FILE.exists(),
        "Data Directory Exists": DATA_DIR.exists(),
        "Outputs Directory Exists": OUTPUTS_DIR.exists(),
    }
    
    all_valid = all(checks.values())
    
    if not all_valid:
        print("❌ Setup validation failed:")
        for check, passed in checks.items():
            status = "✅" if passed else "❌"
            print(f"  {status} {check}")
    else:
        print("✅ All setup checks passed!")
    
    return all_valid


if __name__ == "__main__":
    print("Configuration Settings:")
    print(f"  Model: {MODEL_CONFIG['model_name']}")
    print(f"  Project Root: {PROJECT_ROOT}")
    print(f"  Schema File: {SCHEMA_FILE}")
    print(f"  Data Directory: {DATA_DIR}")
    print()
    validate_setup()
