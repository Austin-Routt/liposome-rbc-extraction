# System Architecture

## Overview

The Literature Review Automation System is a multi-agent architecture designed to extract structured information from scientific PDFs for PRISMA scoping reviews. The system uses Google's Gemini 2.5 Flash Lite model with specialized agents working in coordination.

## Capstone Criteria Compliance

### Course Concepts Used (≥3 Required)

This project demonstrates **5 core concepts** from the Google ADK Agents Intensive course:

#### 1. **Multi-Agent Orchestration** ✅
- **Implementation**: 8 specialized agents coordinated by an orchestrator
- **Evidence**: 
  - Gap, Variable, Technique, and Finding agents work in parallel
  - Assessment agent synthesizes outputs from all extraction agents
  - Validation orchestrator manages quality assurance
- **Course Connection**: Agents Intensive Module on Multi-Agent Systems

#### 2. **Tool Use & Function Calling** ✅
- **Implementation**: Custom tools for PDF processing and validation
- **Evidence**:
  - `pdf_tools.py`: PDF extraction, text search, section identification
  - `text_tools.py`: Normalization, sentence tokenization, unit extraction
  - `validation_tools.py`: Fuzzy matching, schema validation, context checking
- **Course Connection**: Agent Tools & Interoperability with MCP

#### 3. **Structured Prompt Engineering** ✅
- **Implementation**: Detailed, role-based prompts for each agent
- **Evidence**:
  - Step-by-step extraction instructions
  - Context→Thoughts→Summary reasoning pattern
  - Few-shot examples embedded in prompts
  - Output format specifications
- **Course Connection**: Context Engineering & Prompt Design

#### 4. **State Management & Context Handling** ✅
- **Implementation**: Tracking paper processing across agents
- **Evidence**:
  - `PaperProcessingState` object maintains extraction progress
  - Checkpointing for resume capability
  - Context passing between sequential agents
- **Course Connection**: Context Engineering - Sessions & Memory

#### 5. **Quality Assurance & Validation** ✅
- **Implementation**: Multi-layer validation with retry loops
- **Evidence**:
  - Schema validation (structure compliance)
  - Context validation (quote accuracy against PDF)
  - Logic validation (internal consistency)
  - Retry mechanism with configurable attempts
- **Course Connection**: Agent Quality & Evaluation

### Additional Advanced Features

- **Parallel Execution**: Extraction agents run concurrently for efficiency
- **Error Recovery**: Automatic retry with error-specific fixes
- **Confidence Scoring**: Quality metrics for human review thresholds
- **Modular Design**: Agents can be developed and tested independently

## Architecture Diagram

```
┌─────────────────────────────────────────────────────┐
│                  User Interface                      │
│         (Jupyter Notebook / CLI Script)              │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│            Orchestrator (Main Control)               │
│  - Workflow coordination                             │
│  - State management                                  │
│  - Error handling & retry                            │
│  - Progress tracking                                 │
└─────┬───────────────────────────────────────┬───────┘
      │                                       │
      │ Phase 1: Preprocessing                │
      ▼                                       │
┌────────────────────┐                        │
│ Preprocessing      │                        │
│     Agent          │                        │
│                    │                        │
│ Tools:             │                        │
│ - extract_text     │                        │
│ - normalize_text   │                        │
│ - structure_detect │                        │
└─────┬──────────────┘                        │
      │                                       │
      │ Phase 2: Parallel Extraction          │
      ▼                                       │
┌─────────────────────────────────────────────┤
│        Parallel Extraction Pool             │
├─────────────────────────────────────────────┤
│                                             │
│  ┌─────────────┐  ┌──────────────┐        │
│  │    Gap      │  │   Variable   │        │
│  │ Extraction  │  │  Extraction  │        │
│  │    Agent    │  │    Agent     │        │
│  └──────┬──────┘  └──────┬───────┘        │
│         │                │                 │
│  ┌──────┴──────┐  ┌──────┴───────┐        │
│  │  Technique  │  │   Finding    │        │
│  │ Extraction  │  │  Extraction  │        │
│  │    Agent    │  │    Agent     │        │
│  └─────────────┘  └──────────────┘        │
│                                             │
└──────────────────┬──────────────────────────┘
                   │
                   │ Phase 3: Assessment
                   ▼
          ┌────────────────────┐
          │  Final Assessment  │
          │      Agent         │
          │                    │
          │ - Pathway analysis │
          │ - Holistic review  │
          │ - Decision logic   │
          └─────────┬──────────┘
                    │
                    │ Phase 4: Validation
                    ▼
          ┌────────────────────┐
          │   Validation       │
          │   Orchestrator     │
          │                    │
          │ - Schema check     │
          │ - Context check    │
          │ - Logic check      │
          └─────────┬──────────┘
                    │
                    ├─ Valid? ──────┐
                    │                │
                    No               Yes
                    │                │
                    ▼                ▼
          ┌────────────────┐  ┌──────────────┐
          │ Retry with     │  │   Assembly   │
          │ Corrections    │  │    Agent     │
          └────────────────┘  │              │
                    │          │ - Merge data │
                    └──────────│ - QA report  │
                               │ - Save JSON  │
                               └──────────────┘
```

## Agent Specifications

### 1. Preprocessing Agent

**Purpose**: Transform raw PDF into structured, searchable text

**Inputs**:
- PDF file path

**Outputs**:
- Normalized full text
- Text blocks by page
- Document metadata
- Section boundaries

**Key Tools**:
- `extract_text_from_pdf()`
- `normalize_scientific_text()`
- Gemini for structure detection

**Model Usage**:
- Identifies title, authors, journal, year
- Detects section boundaries
- Flags extraction quality issues

### 2. Gap Extraction Agent

**Purpose**: Identify research gaps and limitations

**Inputs**:
- Preprocessed PDF text
- Gap taxonomy

**Outputs**:
- List of gap objects with:
  - Statement, context, thoughts, summary
  - Thematic categorization
  - Gap type, significance

**Key Techniques**:
- Search for limitation/future work sections
- Extract verbatim quotes
- Categorize using gap taxonomy
- Validate against PDF

### 3. Variable Extraction Agent

**Purpose**: Extract measured/calculated variables

**Inputs**:
- Preprocessed PDF text (focus: Methods, Results)
- Variable taxonomy

**Outputs**:
- List of variable objects with:
  - Name, units, method, value range
  - Measurement details
  - Thematic categorization

**Key Techniques**:
- Identify measurement descriptions
- Extract quantitative data
- Categorize by variable type

### 4. Technique Extraction Agent

**Purpose**: Document research methodologies

**Inputs**:
- Preprocessed PDF text (focus: Methods)
- Technique taxonomy

**Outputs**:
- List of technique objects with:
  - Name, materials, procedure
  - Parameters, controls
  - Thematic categorization

### 5. Finding Extraction Agent

**Purpose**: Extract key results and outcomes

**Inputs**:
- Preprocessed PDF text (focus: Results, Discussion)
- Finding taxonomy

**Outputs**:
- List of finding objects with:
  - Statement, quantitative results
  - Conditions, implications
  - Impact direction
  - Thematic categorization

### 6. Final Assessment Agent

**Purpose**: Make inclusion/exclusion decision

**Inputs**:
- All extracted data (gaps, variables, techniques, findings)

**Outputs**:
- Complete final_assessment object with:
  - Pathway analysis (explicit & enhanced)
  - Holistic assessment
  - Final determination

**Decision Logic**:
```
IF has "liposome_rbc_interaction" gap
  → INCLUDE (Pathway 1)
ELSE IF (has liposome_technique AND has rbc_technique) 
     AND (has interaction_variable OR interaction_technique 
          OR interaction_finding OR interaction_gap)
  → INCLUDE (Pathway 2)
ELSE
  → Holistic review for exceptions
```

### 7. Validation Orchestrator Agent

**Purpose**: Ensure data quality

**Validations**:
1. **Schema**: JSON structure compliance
2. **Context**: Quotes match PDF (>90% similarity)
3. **Logic**: Internal consistency

**On Failure**:
- Identifies specific issues
- Triggers targeted retry
- Max 3 retry attempts
- Flags for human review if needed

### 8. Assembly Agent

**Purpose**: Produce final output

**Outputs**:
- Complete JSON file
- Quality assurance report
- Processing log

## Data Flow

### Input Processing

```
PDF File
  ↓
[Preprocessing Agent]
  ↓
Normalized Text + Structure
  ↓
[Distributed to Extraction Agents]
```

### Parallel Extraction

```
                ┌→ [Gap Agent] → Gaps
                │
Preprocessed    ├→ [Variable Agent] → Variables
Text            │
                ├→ [Technique Agent] → Techniques
                │
                └→ [Finding Agent] → Findings
```

### Sequential Assessment

```
All Extractions
  ↓
[Assessment Agent]
  ↓
Final Assessment
  ↓
[Validation Orchestrator]
  ↓
Valid? → Yes → [Assembly Agent] → Final JSON
  │
  No → Retry with Corrections
```

## State Management

### PaperProcessingState

```python
class PaperProcessingState:
    def __init__(self):
        self.pdf_path = None
        self.pdf_data = None
        self.extractions = {
            "gaps": [],
            "variables": [],
            "techniques": [],
            "findings": []
        }
        self.final_assessment = None
        self.validation_results = []
        self.retry_count = 0
        self.status = "initialized"
```

**Checkpoints**:
1. After preprocessing
2. After each extraction agent
3. After assessment
4. After validation
5. After final assembly

**Benefits**:
- Resume from failure
- Track progress
- Audit trail
- Debugging support

## Error Handling Strategy

### Levels of Error Handling

1. **Tool Level**:
   - Try/except in tool functions
   - Fallback mechanisms
   - Logging

2. **Agent Level**:
   - Retry with exponential backoff
   - Alternative approaches
   - Partial results

3. **Orchestrator Level**:
   - Coordination of retries
   - State recovery
   - Human escalation

### Retry Logic

```python
for attempt in range(max_retries):
    try:
        result = agent.process(input_data)
        if validate(result):
            return result
    except Exception as e:
        if attempt < max_retries - 1:
            log_error(e)
            input_data = refine_input(input_data, e)
        else:
            flag_for_human_review()
```

## Performance Optimization

### Parallel Execution

- Extraction agents run concurrently
- 4-way parallelism (gaps, variables, techniques, findings)
- ~4x speedup vs sequential

### Caching Strategy

- Cache PDF extractions
- Cache normalized text
- Cache API responses (future)

### Cost Management

- Model: gemini-2.5-flash-lite (free tier)
- Estimated cost per paper: $0 (free tier)
- Token budget monitoring
- Progressive detail extraction

## Testing Strategy

### Unit Tests

- Test each tool function independently
- Mock API calls
- Test edge cases

### Integration Tests

- Test agent workflows
- Test state management
- Test error recovery

### End-to-End Tests

- Process known papers
- Compare with manual extraction
- Measure accuracy metrics

## Deployment Considerations

### Development (Current)

- Jupyter notebooks for prototyping
- Interactive development
- Immediate feedback

### Production (Future)

- Python scripts for automation
- CLI interface
- Batch processing
- Scheduled execution

### Scaling (Future)

- Database for results
- Web interface
- Multi-user support
- Cloud deployment

## Security & Privacy

- API keys in environment variables
- No sensitive data in code
- PDF content not shared externally
- Local processing preferred

## Future Enhancements

1. **Advanced Features**:
   - Figure/table extraction
   - Citation network analysis
   - Cross-paper relationship mapping

2. **Model Improvements**:
   - Fine-tuning on domain data
   - Ensemble methods
   - Confidence calibration

3. **User Experience**:
   - Web dashboard
   - Real-time progress tracking
   - Interactive validation

4. **Integration**:
   - Reference manager plugins
   - Systematic review software
   - Collaboration tools
