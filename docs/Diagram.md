

# The ASCII Art Version


```ascii

┌─────────────────────────────────────────────────────────────────────────────┐
│                   FULL-TEXT SCREENING PIPELINE ARCHITECTURE                  │
│                          (18-Stage Production System)                         │
└─────────────────────────────────────────────────────────────────────────────┘

INPUT: PDF Research Paper
    │
    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STAGE 0: Multi-Source Study Identifier (Block 7 - Phase 1)                  │
│ ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│ │ PDF Embedded │  │ Programmatic │  │ LLM Holistic │  │ API Validator│    │
│ │   Metadata   │  │  Extraction  │  │  Extraction  │  │  (3 APIs)    │    │
│ │  (PyMuPDF)   │  │ (Regex+OCR)  │  │  (Gemini)    │  │ CrossRef     │    │
│ └──────────────┘  └──────────────┘  └──────────────┘  │ Semantic Sch.│    │
│                                                         │ OpenAlex     │    │
│                           ↓                             └──────────────┘    │
│                  Reconciliation Engine                          ↓           │
│                  (Conflict Resolution + LLM Judgment)                       │
│                           ↓                                                 │
│              Study Identifier (title, authors, year, DOI, journal)          │
└─────────────────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STAGES 1-4: Gaps Processing (Block 3 → Block 4 → Block 5 → Block 6)         │
│                                                                              │
│ Stage 1: EXTRACTION (Block 3 - UnifiedEnumeratorAgent)                      │
│ ┌──────────────────────────────────────────────────────────────────────┐   │
│ │ • Chunk PDF with overlap (prevents boundary loss)                     │   │
│ │ • LLM extraction with section-specific prompts                        │   │
│ │ • Fuzzy quote validation (85% threshold)                              │   │
│ │ • Intelligent retry with feedback                                     │   │
│ │ • Deduplication using composite keys                                  │   │
│ │ Output: ~8 raw gap items                                              │   │
│ └──────────────────────────────────────────────────────────────────────┘   │
│                           ↓                                                 │
│ Stage 2: CONSOLIDATION (Block 4 - ConsolidationAgent)                       │
│ ┌──────────────────────────────────────────────────────────────────────┐   │
│ │ • LLM-based semantic similarity analysis (no embeddings)              │   │
│ │ • Multi-pass shuffled consolidation for large sets                    │   │
│ │ • Quote overlap analysis (50%+ → merge candidate)                     │   │
│ │ • Type-aware grouping (field/methodological/study gaps)               │   │
│ │ • Conservative bias (keep separate when uncertain)                    │   │
│ │ Output: ~3 consolidated gap items                                     │   │
│ └──────────────────────────────────────────────────────────────────────┘   │
│                           ↓                                                 │
│ Stage 3: ENRICHMENT (Block 5 - EnhancedQuoteEnrichmentAgent)                │
│ ┌──────────────────────────────────────────────────────────────────────┐   │
│ │ • Find typed quotes (explanatory, contextual, methodological, etc.)   │   │
│ │ • Citation-aware extraction (preserves all in-text citations)         │   │
│ │ • Fuzzy validation with retry (60%+ → retry, 85%+ → accept)          │   │
│ │ • Citation analysis (detects missing references)                      │   │
│ │ • Duplicate detection separate from validation failures               │   │
│ │ • Rate-limited processing (14 req/min)                               │   │
│ │ Output: ~3 items with 7-12 enriched quotes each                       │   │
│ └──────────────────────────────────────────────────────────────────────┘   │
│                           ↓                                                 │
│ Stage 4: TRANSFORMATION (Block 6 - OptimizedSchemaTransformationCoord.)     │
│ ┌──────────────────────────────────────────────────────────────────────┐   │
│ │ • OptimizedContextHandler: Quotes injected programmatically           │   │
│ │ • LLM generates: thoughts, summary, gap_type, categorization          │   │
│ │ • Section-aware field handling (SectionTypeHandler)                   │   │
│ │ • Checkpoint-based resumption                                         │   │
│ │ • Variables: LLM classifies data_type + measurement_details           │   │
│ │ • Token savings: ~40% (no quote repetition in LLM calls)             │   │
│ │ Output: 3 schema-compliant gap entries                                │   │
│ └──────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STAGES 5-8: Variables Processing (Same 4-stage pipeline)                    │
│ STAGES 9-12: Techniques Processing (Same 4-stage pipeline)                  │
│ STAGES 13-16: Findings Processing (Same 4-stage pipeline)                   │
│                                                                              │
│ Each section goes through: Extract → Consolidate → Enrich → Transform       │
└─────────────────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STAGE 17: Final Assessment (Block 7 - Phase 2)                              │
│                                                                              │
│ Phase A: Pathway Analysis (2 Pathways)                                      │
│ ┌──────────────────────────────────────────────────────────────────────┐   │
│ │ Pathway 1: Explicit Focus                                             │   │
│ │ • Check: Has liposome-RBC interaction gap?                            │   │
│ │ • LLM reasoning: Why does/doesn't this gap exist?                     │   │
│ │ Pathway 2: Enhanced Focus                                             │   │
│ │ • Check foundation: Mentions liposomes + RBCs/erythrocytes?          │   │
│ │ • Check 5 interaction elements across all sections:                  │   │
│ │   - Interaction variables (composition, concentration, etc.)          │   │
│ │   - Morphology variables (size, charge, structure)                   │   │
│ │   - Interaction techniques (incubation, microscopy, etc.)            │   │
│ │   - Interaction findings (hemolysis, fusion, uptake results)         │   │
│ │   - Interaction gaps (limitations in understanding)                  │   │
│ │ • Match if: Foundation + ≥2 elements present                          │   │
│ └──────────────────────────────────────────────────────────────────────┘   │
│                           ↓                                                 │
│ Phase B: Holistic Assessment                                                │
│ ┌──────────────────────────────────────────────────────────────────────┐   │
│ │ LLM analyzes entire document:                                         │   │
│ │ • Classify interaction level: Primary/Substantial/Peripheral/Not      │   │
│ │ • Consider: Paper's main focus, depth of interaction coverage         │   │
│ │ • Reasoning: Step-by-step explanation of classification               │   │
│ └──────────────────────────────────────────────────────────────────────┘   │
│                           ↓                                                 │
│ Phase C: Final Determination                                                │
│ ┌──────────────────────────────────────────────────────────────────────┐   │
│ │ Decision Logic:                                                        │   │
│ │ • Include: IF (Pathway 1 OR Pathway 2) AND Interaction ≥ Substantial │   │
│ │ • Exclude: Otherwise                                                  │   │
│ │ • Priority: "High" if Primary, "Medium" if Substantial, else "Low"   │   │
│ │ • Exception handling: Allow override with justification               │   │
│ │ Output: Final determination with full reasoning chain                 │   │
│ └──────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STAGE 18: Document Assembly & Validation                                    │
│ • Combine all sections + study identifier + final assessment                │
│ • Remove internal metadata (_source_metadata, etc.)                         │
│ • Validate against JSON schema                                              │
│ • Save as schema-compliant JSON document                                    │
└─────────────────────────────────────────────────────────────────────────────┘
    │
    ▼
OUTPUT: Complete Schema-Compliant Document
{
  "study_identifier": {...},
  "gaps": [...],
  "variables": [...],
  "techniques": [...],
  "findings": [...],
  "final_assessment": {
    "pathway_analysis": {...},
    "holistic_assessment": {...},
    "final_determination": {...}
  }
}

┌─────────────────────────────────────────────────────────────────────────────┐
│                        CROSS-CUTTING CAPABILITIES                            │
├─────────────────────────────────────────────────────────────────────────────┤
│ • Rate Limiting: 14 req/min (safe for free tier) across all LLM calls       │
│ • Checkpointing: Resume from any failed stage                               │
│ • Observability: Comprehensive logging + debug logs per stage               │
│ • Error Handling: Graceful degradation + fallback mechanisms                │
│ • Quote Validation: Fuzzy matching (85% threshold) prevents false positives │
│ • Session Management: Proper ADK pattern throughout                         │
└─────────────────────────────────────────────────────────────────────────────┘

```

# Wide Screen


![Wide Screen Full Text Screening Pipeline Diagram](images/Wide%20Screen%20Full%20Text%20Screening%20Pipeline%20Diagram.jpg)



# Vertical

![Vertical Full Text Screening Pipeline Diagram](images/Full%20Text%20Screening%20Pipeline%20Diagram.jpg)







