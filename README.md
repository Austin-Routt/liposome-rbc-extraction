# Multi-Agent Literature Review Automation System

**Automated Extraction of Structured Information from Scientific PDFs for PRISMA Scoping Reviews**

## Overview

This system automates the extraction of structured data from scientific literature on liposome-RBC interactions. Using a multi-agent architecture powered by Google's Gemini 2.5 Flash Lite, the system processes PDF documents and generates schema-compliant JSON outputs suitable for systematic literature reviews.

## Project Context

- **Course**: Google ADK Agents Intensive Capstone Project
- **Application**: PhD Literature Review on Liposome-Red Blood Cell Interactions
- **Goal**: Automate extraction and validation of research gaps, variables, techniques, findings, and inclusion decisions

## Architecture

### Multi-Agent System
- **Preprocessing Agent**: PDF text extraction and normalization
- **Gap Extraction Agent**: Identifies research gaps and limitations
- **Variable Extraction Agent**: Extracts measured variables and data
- **Technique Extraction Agent**: Documents research methodologies
- **Finding Extraction Agent**: Captures key results and outcomes
- **Assessment Agent**: Makes inclusion/exclusion decisions
- **Validation Orchestrator**: Ensures data quality and accuracy
- **Assembly Agent**: Produces final validated JSON output

### Course Concepts Demonstrated
1. **Multi-Agent Orchestration**: Coordinated specialist agents
2. **Tool Use & Function Calling**: PDF processing, validation tools
3. **Prompt Engineering**: Structured extraction prompts
4. **Context Management**: State tracking across processing pipeline
5. **Quality Assurance**: Validation loops and error handling

## Project Structure

```
liposome-rbc-extraction/
├── notebooks/          # Jupyter notebooks for development
├── src/                # Production Python modules
│   ├── agents/        # Agent implementations
│   ├── tools/         # Tool functions
│   └── utils/         # Utilities and helpers
├── tests/             # Unit and integration tests
├── data/              # Schemas, samples, outputs
├── config/            # Configuration files
├── docs/              # Documentation
└── scripts/           # CLI scripts
```

## Requirements

- Python 3.10+
- Google AI Python SDK
- PyMuPDF (fitz)
- Additional dependencies in `requirements.txt`

## Setup

```bash
# Clone repository
git clone <repository-url>
cd liposome-rbc-extraction

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up API key
export GOOGLE_API_KEY="your-api-key-here"
```

## Development Workflow

### Phase 1: Notebook Development (Current)
Develop and test individual agents in Jupyter notebooks:
```bash
jupyter notebook notebooks/
```

### Phase 2: Script Migration (Future)
Refactor working code into production modules in `src/`

### Phase 3: Integration (Future)
Complete end-to-end pipeline with CLI interface

## Usage (Planned)

```python
from src.orchestrator import PaperProcessor

# Process a single paper
processor = PaperProcessor(model="gemini-2.5-flash-lite")
result = processor.process_paper("path/to/paper.pdf")

# Access validated output
print(result.json_output)
print(result.validation_report)
```

## Model Information

**Using**: `gemini-2.5-flash-lite`
- Free tier model
- Fast and cost-effective
- Suitable for structured extraction tasks

## Validation

The system includes three layers of validation:
1. **Schema Validation**: JSON structure compliance
2. **Context Validation**: Quote accuracy vs. PDF source
3. **Logic Validation**: Internal consistency checks

## Project Status

🚧 **In Development** 🚧

- [x] Project setup and architecture design
- [ ] PDF preprocessing agent (Week 1-2)
- [ ] Gap extraction agent (Week 3)
- [ ] Variable extraction agent (Week 4)
- [ ] Technique extraction agent (Week 4)
- [ ] Finding extraction agent (Week 5)
- [ ] Assessment agent (Week 6)
- [ ] Validation orchestrator (Week 6)
- [ ] Assembly agent (Week 7)
- [ ] End-to-end integration (Week 7)
- [ ] Documentation and testing (Week 8)

## Contributing

This is a capstone project. Feedback and suggestions welcome via issues.

## License

Academic use - MIT License (TBD)

## Contact

[Your Name]
[Your Institution]
[Contact Information]

---

**Last Updated**: 2024
