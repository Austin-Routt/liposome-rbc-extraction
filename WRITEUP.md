
![](https://www.googleapis.com/download/storage/v1/b/kaggle-user-content/o/inbox%2F450172%2F74bf047162ef52d3724540a4f79cbef3%2FProblem-solution.jpg?generation=1764373152845429&alt=media)

## Problem Statement

**The Core Challenge:**
Academic information extraction requires deep semantic comprehension that goes far beyond keyword matching or simple classification. When screening research papers for literature reviews, experts must:

- **Distinguish between what authors studied vs. what they merely cited** (e.g., "Smith et al. found X" vs. "We investigated X")
- **Identify genuine research gaps vs. methodological choices** (e.g., "No studies have examined X" vs. "We chose not to examine X")
- **Preserve citation provenance** while extracting quotes (maintaining in-text citations like "(Smith 2020)" throughout processing)
- **Make explainable inclusion/exclusion decisions** based on complex pathway logic and holistic assessment

#### Traditional NLP Approaches & Manual Review both have issues

Traditional NLP approaches fail because they lack contextual understanding. Manual review works but suffers from:
- **Inter-rater variability** 
- **Unstructured outputs** (scattered notes across Word documents, no schema compliance)
- **No provenance tracking** (can't audit why decisions were made)
- **Inconsistent criteria application** (fatigue, confirmation bias, subjective interpretation)


#### **Why This Matters:**
Literature reviews synthesize evidence from hundreds of papers to inform clinical guidelines, policy decisions, and research agendas. The quality of evidence synthesis directly impacts healthcare, environmental policy, and scientific progress. Yet the screening process is a critical bottleneck with quality-vs-speed trade-offs.



## Why Agents?

**Why Multi-Agent Orchestration is Essential:**

### 1. **Sequential Specialization Enables Quality Control**
A single monolithic LLM call to "extract everything from this paper based on this schema" produces inconsistent, unverifiable results. Breaking the task into specialized stages allows:
- **Extraction Agent**: Focus purely on finding items (gaps, variables, techniques, findings)
- **Consolidation Agent**: Semantic deduplication using LLM reasoning
- **Enrichment Agent**: Quote finding with citation preservation
- **Transformation Agent**: Schema compliance and data type classification

Each agent has a **single responsibility** with **explicit validation criteria**, enabling targeted retry and quality assurance.


### 2. **Complex Orchestration Handles Failure Gracefully**
Academic PDFs are messy: poor OCR, formatting variations, missing sections. A 200-paper review cannot fail completely if paper #47 has extraction issues. The solution requires:
- **Checkpoint-based resumption**: 18-stage pipeline with stage-level recovery
- **Graceful degradation**: Continue processing with fallback identifiers if API validation fails
- **Intelligent retry**: Citation-aware retry when enrichment detects stripped references

This level of fault tolerance requires **orchestrated agents with shared state management**, not a single agent.

### 3. **Agents Enable Explainability**
Black-box classification ("Include: Yes/No") is unacceptable for explainable literature reviews. The solution requires:
- **Pathway Analysis**: Explicit focus (gap statement matching) + Enhanced focus (specific variables, techniques, or findings)
- **Holistic LLM assessment**: Classification of the entire paper with reasoning
- **Final determination**: Combining both signals with exception handling

This **multi-step reasoning** with **intermediate decisions** is naturally expressed as an agent workflow, not a single prompt.

**Bottom Line:** Agents aren't just convenient—they're **architecturally necessary** for quality assurance,  fault tolerance, and explainability in complex semantic extraction.

---

## What was Created

### **Architecture: 18-Stage Multi-Agent Pipeline**

```
INPUT: Academic Paper (PDF)
   ↓
┌─────────────────────────────────────────────┐
│ Stage 0: Multi-Source Study Identifier      │
│ ┌─────────┐ ┌─────────┐ ┌─────────┐         │
│ │  PDF    │ │  Local  │ │   API   │         │
│ │Metadata │ │ Extract │ │Validate │         │
│ └─────────┘ └─────────┘ └─────────┘         │
│         Reconciliation Engine               │
└─────────────────────────────────────────────┘
   ↓
┌─────────────────────────────────────────────┐
│ Stages 1-16: Section Processing (×4)        │
│ For: Gaps, Variables, Techniques, Findings  │
│                                             │
│ Stage N+0: Extract → Fuzzy Validation       │
│ Stage N+1: Consolidate → LLM Deduplication  │
│ Stage N+2: Enrich → Quote + Citation Check  │
│ Stage N+3: Transform → Schema Compliance    │
└─────────────────────────────────────────────┘
   ↓
┌─────────────────────────────────────────────┐
│ Stage 17: Final Assessment                  │
│ Pathway Analysis + Holistic + Determination │
└─────────────────────────────────────────────┘
   ↓
OUTPUT: Schema-Compliant JSON Document
```

![](https://www.googleapis.com/download/storage/v1/b/kaggle-user-content/o/inbox%2F450172%2Fb4be0cb5df3f0febf32b122eb858ab7c%2FFull%20Text%20Screening%20Pipeline%20Diagram.jpg?generation=1764373763455661&alt=media)



## Demo

### **Sample Input:**
*"In vitro interactions of liposomes with erythrocytes: Relevance to drug delivery systems"*  
(14-page biomedical research paper)

### **Processing:**
- **Time**: 3-5 hours (varies with paper complexity)
- **Total Items Extracted**: 100 (3 gaps, 45 variables, 40 techniques, 12 findings)
- **Validation Scores**: 85-92% fuzzy match accuracy across sections

### **Sample Extracted Gap:**
```json
{
  "gap_statement": "Limited understanding of in vivo liposome-RBC aggregate behavior",
  "gap_significance": "High",
  "gap_type": "Insufficient empirical evidence",
  "evidence_level": "Strong",
  "quotes": [
    {
      "quote_text": "The in vivo behavior of these aggregates remains poorly understood",
      "page_number": 12,
      "quote_type": "explanatory",
      "validation_score": 0.94
    }
    // ... 8 more supporting quotes with citations preserved
  ]
}
```

### **Sample Extracted Variable:**
```json
{
  "variable_name": "DOTAP concentration",
  "variable_context": "Cationic lipid used in liposome formulation",
  "data_type": "CONTINUOUS",
  "quotes": [
    {
      "quote_text": "DOTAP concentrations ranging from 10-50 mol%",
      "page_number": 4,
      "quote_type": "technical_detail"
    }
  ]
}
```

### **Final Assessment:**
```json
{
  "determination": "INCLUDE",
  "priority_level": "High",
  "pathway_1_explicit_match": true,
  "pathway_2_enhanced_match": true,
  "holistic_assessment": "Primary focus",
  "reasoning": [
    "Paper explicitly identifies gap in liposome-RBC interaction understanding",
    "Foundation established + 4/5 interaction types present across sections",
    "Main objective aligns with review focus area"
  ]
}
```

### **Output:**
Schema-compliant JSON.

---

## The Build

### **ADK Concepts Implemented:**

#### **1. Multi-Agent Systems** (Sequential, Parallel, Complex Orchestration)

**Sequential Agents:**
```python
# 4-stage pipeline per section type
section_pipeline = SequentialAgent(
    name=f"{section_type}_pipeline",
    sub_agents=[
        extractor_agent,      # Stage N+0
        consolidator_agent,   # Stage N+1
        enricher_agent,       # Stage N+2
        transformer_agent     # Stage N+3
    ]
)
```

**Parallel Agents:**
```python
# 5-source study identifier with concurrent API calls
api_results = await asyncio.gather(
    validate_with_crossref(doi),
    validate_with_semantic_scholar(doi),
    validate_with_openalex(doi)
)
```

**Complex Orchestration:**
```python
# 18-stage pipeline with checkpoint resumption
pipeline_stages = [
    study_identifier,         # Stage 0
    *gaps_pipeline,          # Stages 1-4
    *variables_pipeline,     # Stages 5-8
    *techniques_pipeline,    # Stages 9-12
    *findings_pipeline,      # Stages 13-16
    final_assessment         # Stage 17
]
```

#### **2. Custom Tools**

**PDF Processing:**
```python
class PDFProcessor:
    def verify_quotes_fuzzy(self, quote: str, threshold=85):
        """Multi-algorithm fuzzy matching with normalized text"""
        scores = [
            fuzz.ratio(quote, sentence),
            fuzz.partial_ratio(quote, sentence),
            fuzz.token_sort_ratio(quote, sentence)
        ]
        return max(scores)
```

**API Integration:**
```python
class APIValidator:
    async def validate_with_apis(self, doi: str):
        """Concurrent validation across 3 sources"""
        async with httpx.AsyncClient() as client:
            return await self._parallel_fetch([
                CrossRefAPI, SemanticScholarAPI, OpenAlexAPI
            ])
```

#### **3. Sessions & Memory**

**Session Management:**
```python
try:
    session = runner.create_session()
except Exception:
    # Handle re-run error gracefully
    session = existing_session
```

**Checkpoint System:**
```python
class CheckpointManager:
    def save_progress(self, stage_num, results):
        checkpoint = {
            "stage": stage_num,
            "timestamp": datetime.now(),
            "results": results
        }
        self._atomic_write(checkpoint)
```

#### **4. Rate Limiting & Observability**

**Rate Limiter:**
```python
class RateLimiter:
    def __init__(self, rate=14):  # Free tier safe
        self.delay = 60 / rate
        self.lock = asyncio.Lock()
```

**Observability:**
- Stage-level duration tracking
- Validation score logging: "Validated 8/10 quotes, avg 0.92"
- Comprehensive debug logs per stage

### **Technologies Used:**
- **Framework**: Google ADK (Agent Development Kit)
- **Model**: Gemini 2.5 Flash Lite
- **PDF Processing**: PyMuPDF
- **Validation**: jsonschema, fuzzywuzzy, Levenshtein distance
- **APIs**: CrossRef, Semantic Scholar, OpenAlex
- **Environment**: Jupyter Notebook with nest_asyncio

---

## If I Had More Time, This is What I'd Do

### **1. Speed Optimization** (Address the 3-5 hour bottleneck)
**Current bottleneck:** Each item requires 2-3 minutes of sequential LLM calls (extract → consolidate → enrich → transform).

**Solution:** Parallel processing of the key Loop (extract → consolidate → enrich → transform)
```python
# Instead of: Looping 4 time for Gaps, Variables, Techniques, and Findings
# Do: Create 4 parallel loops that run concurrently,

```
**Expected improvement:** 3-5 hours → 45-90 minutes


### **2. Cloud Deployment**
**Current limitation:** Local Jupyter notebook only

**Solution:** Containerized API endpoint for batch processing of entire review libraries (200+ papers)

### **3. Expand to Additional Research Domains**
**Current limitation:** Tested only on red blood cell and liposome interaction papers

**Solution:** Domain-agnostic schema with configurable section types for social sciences, engineering, etc.


