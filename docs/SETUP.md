# Project Setup Guide

## Quick Start

### 1. Clone and Setup Environment

```bash
# Clone repository
git clone <repository-url>
cd liposome-rbc-extraction

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Unix/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Configure API Key

Create a `.env` file in the project root:

```bash
# .env
GOOGLE_API_KEY=your_api_key_here
```

Get your API key from: https://makersuite.google.com/app/apikey

### 3. Add Schema and Sample Data

```bash
# Add the full-text screening schema
cp path/to/fulltext_screening_schema.json data/schemas/

# Add sample PDFs for testing
cp path/to/sample.pdf data/sample_pdfs/
```

### 4. Install NLTK Data

```python
import nltk
nltk.download('punkt')
```

### 5. Verify Setup

```bash
python src/utils/config.py
```

Should show:
```
✅ All setup checks passed!
```

## Development Workflow

### Phase 1: Notebook Development (Weeks 1-4)

Start with Jupyter notebooks for rapid prototyping:

```bash
jupyter notebook notebooks/
```

**Notebook Sequence:**
1. `01_pdf_preprocessing.ipynb` - PDF extraction and normalization
2. `02_gap_extraction.ipynb` - Research gap identification
3. `03_variable_extraction.ipynb` - Variable measurement extraction
4. `04_technique_extraction.ipynb` - Methodology documentation
5. `05_finding_extraction.ipynb` - Results extraction
6. `06_final_assessment.ipynb` - Inclusion/exclusion decision
7. `07_validation.ipynb` - Validation orchestration
8. `08_end_to_end_pipeline.ipynb` - Complete workflow

### Phase 2: Script Migration (Weeks 5-7)

Refactor working notebook code into production modules:

```bash
src/
├── agents/
│   ├── preprocessing_agent.py      # From notebook 01
│   ├── gap_extraction_agent.py     # From notebook 02
│   ├── variable_extraction_agent.py # From notebook 03
│   └── ...
```

### Phase 3: Integration (Week 8)

Build complete pipeline:

```bash
python src/main.py --pdf path/to/paper.pdf --output results.json
```

## Project Structure

```
liposome-rbc-extraction/
├── README.md                  # Project overview
├── requirements.txt           # Python dependencies
├── .env                       # API keys (not in git)
├── .gitignore                # Git ignore rules
│
├── notebooks/                 # Development notebooks
│   ├── 01_pdf_preprocessing.ipynb
│   ├── 02_gap_extraction.ipynb
│   └── ...
│
├── src/                       # Production code
│   ├── agents/               # Agent implementations
│   ├── tools/                # Utility functions
│   ├── utils/                # Configuration & helpers
│   ├── orchestrator.py       # Main orchestration logic
│   └── main.py               # CLI entry point
│
├── tests/                     # Unit tests
│   ├── test_pdf_tools.py
│   └── ...
│
├── data/                      # Data files
│   ├── schemas/              # JSON schemas
│   ├── sample_pdfs/          # Test PDFs
│   ├── outputs/              # Generated outputs
│   └── validation_reports/   # Validation results
│
├── config/                    # Configuration files
│   └── agent_prompts.yaml    # Prompt templates
│
└── docs/                      # Documentation
    ├── architecture.md        # System architecture
    ├── agent_specifications.md # Agent details
    └── usage_guide.md         # User guide
```

## Common Tasks

### Run a Single Agent

```python
from src.agents.gap_extraction_agent import GapExtractionAgent
from src.tools.pdf_tools import extract_text_from_pdf

# Extract PDF
pdf_data = extract_text_from_pdf("paper.pdf")

# Run agent
agent = GapExtractionAgent()
gaps = agent.extract_items(pdf_data)
print(f"Found {len(gaps)} research gaps")
```

### Validate Extracted Data

```python
from src.tools.validation_tools import validate_json_schema

# Load schema
with open("data/schemas/fulltext_screening_schema.json") as f:
    schema = json.load(f)

# Validate
result = validate_json_schema(extracted_data, schema)
if result["valid"]:
    print("✅ Valid")
else:
    print("❌ Errors:", result["errors"])
```

### Process Multiple Papers

```bash
python scripts/batch_process.py \
  --input-dir data/sample_pdfs/ \
  --output-dir data/outputs/ \
  --report
```

## Troubleshooting

### API Key Issues

**Problem**: `GOOGLE_API_KEY not set`

**Solution**: 
1. Create `.env` file in project root
2. Add: `GOOGLE_API_KEY=your_key_here`
3. Restart Python kernel/notebook

### PDF Extraction Errors

**Problem**: `Error extracting text from PDF`

**Solutions**:
- Check PDF is not corrupted
- Try re-downloading PDF
- Check PDF is not password-protected
- Ensure PyMuPDF installed: `pip install PyMuPDF`

### NLTK Data Missing

**Problem**: `LookupError: Resource punkt not found`

**Solution**:
```python
import nltk
nltk.download('punkt')
```

### FuzzyWuzzy Performance

For better performance, install python-Levenshtein:
```bash
pip install python-Levenshtein
```

### Model Response Errors

**Problem**: Empty or invalid JSON responses

**Solutions**:
1. Check API key is valid and has quota
2. Reduce input text length
3. Increase max_output_tokens in config
4. Check prompt formatting

## Best Practices

### When Developing in Notebooks

1. **Always test with small examples first**
2. **Save intermediate outputs** for debugging
3. **Document your findings** in markdown cells
4. **Test edge cases** (empty sections, malformed text)
5. **Track costs** - even free tier has limits

### When Refactoring to Scripts

1. **Add comprehensive error handling**
2. **Write unit tests** for each function
3. **Add logging statements**
4. **Document functions** with docstrings
5. **Keep configuration separate** from code

### Performance Optimization

1. **Use caching** for repeated API calls
2. **Process in batches** when possible
3. **Parallel execution** for independent tasks
4. **Progressive detail** extraction (coarse then fine)

## Getting Help

- **Documentation**: See `docs/` directory
- **Issues**: Check existing issues on GitHub
- **Contact**: [Your contact information]

## Next Steps

1. Complete `01_pdf_preprocessing.ipynb`
2. Validate on multiple sample PDFs
3. Proceed to gap extraction
4. Build iteratively, testing at each stage
