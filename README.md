
# Full-Text Literature Review Screening System
*Google ADK Capstone Project - Freestyle Agents Track*


![Problem->Solution](docs/images/animated%20problem%20solution.gif)


**An automated fulltext screening system for literature reviews using Google ADK.**

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Google ADK](https://img.shields.io/badge/Google-ADK-4285F4.svg)](https://github.com/google/adk)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Overview

This system automates full-text screening for a PRISMA scoping literature review inovolving Red Blood Cell & Liposome interactions, processing research papers through 18 integrated stages to extract structured metadata, research gaps, variables, techniques, and findings, culminating in explainable inclusion & exclusion decisions.


### What It Does
```
INPUT:  Academic paper (PDF)
        ↓
OUTPUT: Schema-compliant JSON document with:
        • Study metadata (validated across 5 sources)
        • Research gaps (with thematic categorization)
        • Variables (with data type classification)
        • Experimental techniques
        • Key findings
        • Inclusion/exclusion determination (holistic & pathway-based)
```



## Problem
Literature reviews require screening hundreds of papers, taking 60-90 minutes per paper.


## Solution
An automated screening system using Google ADK with 18-stage pipeline processing PDFs through multi-agent workflows.

## Architecture

### Vertical Full Text Screening Pipeline Diagram

![Vertical Full Text Screening Pipeline Diagram](docs/images/Full%20Text%20Screening%20Pipeline%20Diagram.jpg)


### Wide Screen Full Text Screening Pipeline Diagram

![Wide Screen Full Text Screening Pipeline Diagram](docs/images/Wide%20Screen%20Full%20Text%20Screening%20Pipeline%20Diagram.jpg)



**Pipeline Overview:**
- Stage 0: Multi-source study identifier (6 parallel sources)
- Stages 1-16: Section processing (gaps, variables, techniques, findings)
  - Each: Extract → Consolidate → Enrich → Transform
- Stage 17: Final assessment (pathway analysis + holistic judgment)
- Stage 18: Document assembly & validation




## Quick Start

**Prerequisites:**
- Python 3.10+
- Google API key (for Gemini)
- Jupyter Notebook environment

**Installation:**
```bash
pip install google-adk PyMuPDF httpx jsonschema nltk fuzzywuzzy python-Levenshtein nest-asyncio tqdm
```

**Usage:**
1. Open `notebooks/Full Text Screener Prototype.ipynb`
2. Set your API key: `os.environ['GOOGLE_API_KEY'] = 'your-key'`
3. Run Code Block cells to initialize all blocks
4. Run final cell to process PDFs:


## Performance
- **Processing time**: 3-5 hours per paper (tested on 3 papers)
- **Per Item**: 2-3 minutes per extracted item
- **Fast papers** (<20 items): ~1 hour
- **Complex papers** (>100 items): 3+ hours

## ADK Concepts Implemented

### 1. Multi-Agent Systems (Sequential, Parallel, Complex Orchestration)
- **Sequential**: 4-stage pipeline per section (Extract → Consolidate → Enrich → Transform)
- **Parallel**: 5-source study identifier with concurrent API calls
- **Complex**: 18-stage orchestration with checkpoint resumption


### 2. Sessions & Memory
- **Session Management**: Proper ADK pattern with error handling
- **Checkpoint System**: Stage-level resumption
- **Cross-stage Context**: Quote preservation and injection

### 3. Rate Limiting & Observability
- **Rate Limiter**: 14 req/min enforcement (free tier safe)
- **Observability**: Comprehensive logging, debug logs per stage
- **Monitoring**: Stage duration, success/failure statistics

### 4. Advanced Validation & Retry
- **Multi-level Validation**: Fuzzy matching (85%), schema, citations
- **Intelligent Retry**: Citation-aware retry with feedback
- **Quality Assurance**: Validation score tracking

## Output Format
Schema-compliant JSON with:
- `study_identifier`: Validated metadata
- `gaps[]`: Research gaps with quotes
- `variables[]`: Experimental variables
- `techniques[]`: Methods and procedures
- `findings[]`: Results and conclusions
- `final_assessment`: Inclusion decision with reasoning

## Basic Project Structure
````
notebooks/
  └── Full Text Screener Prototype.ipynb  # Main implementation
data/
  ├── schemas/
  │   └── fulltext_screening_schema.json
  ├── sample_pdfs/
  └── outputs/                            # Generated results
````

## Development
Built using:
- **Framework**: Google ADK (Agent Development Kit)
- **Model**: Gemini 2.5 Flash Lite
- **PDF Processing**: PyMuPDF
- **Validation**: jsonschema, fuzzywuzzy
- **APIs**: CrossRef, Semantic Scholar, OpenAlex



## Citation

If you use this pipeline in your research, please cite:
```bibtex
@software{fulltext_screening_pipeline_2025,
  title={Full-Text Literature Review Screening Pipeline},
  author={Austin Harper Routt},
  year={2025},
  url={https://github.com/Austin-Routt/liposome-rbc-extraction}
}
```

---

## License

MIT License - see LICENSE file for details

---

## Acknowledgments

- Built with [Google ADK](https://github.com/google/adk)
- Uses [PyMuPDF](https://pymupdf.readthedocs.io/) for PDF processing
- API validation via [CrossRef](https://www.crossref.org/), [Semantic Scholar](https://www.semanticscholar.org/), and [OpenAlex](https://openalex.org/)
