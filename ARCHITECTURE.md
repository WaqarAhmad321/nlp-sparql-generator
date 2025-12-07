# System Architecture Diagram

## Data Flow Visualization

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│                        USER INTERFACE                            │
│                       (Streamlit Web App)                        │
│                                                                  │
│  ┌──────────────────────────────────────────────────────┐      │
│  │  Input: "List all customers in India"                │      │
│  │  [Submit Button]                                       │      │
│  └──────────────────────────────────────────────────────┘      │
│                          │                                       │
└──────────────────────────┼───────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    NLP PROCESSOR                                 │
│                   (nlp_processor.py)                             │
│                                                                  │
│  Step 1: Tokenization                                           │
│    "List all customers in India"                                │
│    → ["list", "all", "customers", "in", "india"]               │
│                                                                  │
│  Step 2: Lemmatization                                          │
│    ["list", "all", "customers", "in", "india"]                 │
│    → ["list", "all", "customer", "in", "india"]                │
│                                                                  │
│  Step 3: Entity Detection                                       │
│    Classes: ["Customer"]                                        │
│    Properties: ["fullName"]                                     │
│    Filters: {"basedIn": "India"}                               │
│                                                                  │
│  Step 4: Intent Recognition                                     │
│    Intent: "list"                                               │
│                                                                  │
│  Output: {                                                      │
│    "classes": ["Customer"],                                     │
│    "properties": ["fullName"],                                  │
│    "filters": {"basedIn": "India"},                            │
│    "intent": "list"                                             │
│  }                                                              │
│                                                                  │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                  SPARQL GENERATOR                                │
│                (sparql_generator.py)                             │
│                                                                  │
│  Step 1: Select Query Template                                  │
│    Pattern: Customer + Country Filter                           │
│                                                                  │
│  Step 2: Build SPARQL Query                                     │
│    PREFIX cccm: <http://www.semanticweb.org/cccm#>            │
│    SELECT ?name                                                 │
│    WHERE {                                                      │
│      ?cust a cccm:Customer ;                                    │
│            cccm:fullName ?name ;                                │
│            cccm:basedIn cccm:India .                           │
│    }                                                            │
│                                                                  │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                  RDF QUERY EXECUTOR                              │
│                (rdf_query_executor.py)                           │
│                                                                  │
│  Step 1: Load RDF Graph                                         │
│    File: CCCM PERFECTED.owl                                     │
│    Triples: 5000+ loaded                                        │
│                                                                  │
│  Step 2: Execute SPARQL                                         │
│    Run query on RDF graph                                       │
│                                                                  │
│  Step 3: Extract Results                                        │
│    Results:                                                     │
│    - Amit Patel                                                 │
│    - Kiran Desai                                                │
│    - Ashok Patil                                                │
│    - ... (more results)                                         │
│                                                                  │
│  Step 4: Convert to DataFrame                                   │
│    ┌─────────────────┐                                         │
│    │  name           │                                          │
│    ├─────────────────┤                                         │
│    │  Amit Patel     │                                          │
│    │  Kiran Desai    │                                          │
│    │  Ashok Patil    │                                          │
│    └─────────────────┘                                         │
│                                                                  │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    RESULTS DISPLAY                               │
│                   (Streamlit UI)                                 │
│                                                                  │
│  ┌─────────────────────────────────────────────────────┐       │
│  │ Tab 1: Results                                       │       │
│  │ ┌─────────────────┐                                 │       │
│  │ │  name           │                                  │       │
│  │ ├─────────────────┤                                 │       │
│  │ │  Amit Patel     │                                  │       │
│  │ │  Kiran Desai    │                                  │       │
│  │ │  Ashok Patil    │                                  │       │
│  │ └─────────────────┘                                 │       │
│  │ [Download CSV]                                       │       │
│  └─────────────────────────────────────────────────────┘       │
│                                                                  │
│  ┌─────────────────────────────────────────────────────┐       │
│  │ Tab 2: SPARQL Query                                  │       │
│  │ PREFIX cccm: <...>                                   │       │
│  │ SELECT ?name WHERE { ... }                           │       │
│  └─────────────────────────────────────────────────────┘       │
│                                                                  │
│  ┌─────────────────────────────────────────────────────┐       │
│  │ Tab 3: NLP Analysis                                  │       │
│  │ - Tokens: [list, all, customer, ...]                │       │
│  │ - Classes: [Customer]                                │       │
│  │ - Filters: {basedIn: India}                         │       │
│  └─────────────────────────────────────────────────────┘       │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## Component Interactions

```
┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│              │       │              │       │              │
│   app.py     │──────▶│ nlp_processor│──────▶│   sparql_    │
│ (Streamlit)  │       │    .py       │       │  generator.py│
│              │       │              │       │              │
└──────┬───────┘       └──────────────┘       └──────┬───────┘
       │                                              │
       │                                              │
       │               ┌──────────────┐              │
       │               │              │              │
       └──────────────▶│ rdf_query_   │◀─────────────┘
                       │ executor.py  │
                       │              │
                       └──────┬───────┘
                              │
                              ▼
                       ┌──────────────┐
                       │ CCCM Dataset │
                       │  (.owl file) │
                       └──────────────┘
```

---

## NLP Processing Pipeline

```
Input Query
    │
    ├─▶ Tokenization
    │      ↓
    ├─▶ Lemmatization
    │      ↓
    ├─▶ Stopword Removal
    │      ↓
    ├─▶ POS Tagging
    │      ↓
    ├─▶ Class Detection ──▶ ["Customer", "Transaction", ...]
    │      ↓
    ├─▶ Property Detection ──▶ ["fullName", "basedIn", ...]
    │      ↓
    ├─▶ Filter Detection ──▶ {"basedIn": "India", ...}
    │      ↓
    ├─▶ Intent Detection ──▶ "list", "count", etc.
    │      ↓
    └─▶ Aggregation Detection ──▶ "COUNT", "SUM", etc.
            ↓
    Structured Output
```

---

## SPARQL Generation Process

```
NLP Result
    │
    ├─▶ Analyze Classes
    │      ↓
    ├─▶ Analyze Properties
    │      ↓
    ├─▶ Analyze Filters
    │      ↓
    ├─▶ Select Query Pattern
    │      │
    │      ├─▶ Customer Query?
    │      ├─▶ Transaction Query?
    │      ├─▶ Institution Query?
    │      ├─▶ Aggregation Query?
    │      └─▶ Default Query?
    │      ↓
    ├─▶ Build PREFIX
    │      ↓
    ├─▶ Build SELECT Clause
    │      ↓
    ├─▶ Build WHERE Clause
    │      │
    │      ├─▶ Add Class Patterns
    │      ├─▶ Add Property Patterns
    │      └─▶ Add Filters
    │      ↓
    ├─▶ Add GROUP BY (if needed)
    │      ↓
    ├─▶ Add ORDER BY (if needed)
    │      ↓
    └─▶ Complete SPARQL Query
```

---

## File Dependencies

```
app.py
  ├── imports: streamlit, pandas
  ├── imports: nlp_processor.NLPProcessor
  ├── imports: sparql_generator.SPARQLGenerator
  └── imports: rdf_query_executor.RDFQueryExecutor

nlp_processor.py
  ├── imports: spacy
  └── imports: re

sparql_generator.py
  └── imports: typing

rdf_query_executor.py
  ├── imports: rdflib
  └── imports: pandas

test_queries.py
  ├── imports: nlp_processor.NLPProcessor
  └── imports: sparql_generator.SPARQLGenerator
```

---

## Vocabulary Mapping Structure

```
User Input: "customers in India"
              ↓
        ┌─────┴─────┐
        │           │
    "customers"  "India"
        │           │
        ▼           ▼
   Class Map    Country Map
        │           │
        ▼           ▼
   "Customer"   "India"
        │           │
        └─────┬─────┘
              ↓
        RDF Entities
        cccm:Customer
        cccm:India
```

---

## Query Execution Flow

```
1. User Types Query
         ↓
2. Submit Button Clicked
         ↓
3. NLP Processing (2-5ms)
         ↓
4. SPARQL Generation (1-2ms)
         ↓
5. RDF Query Execution (10-100ms)
         ↓
6. Results Conversion (1-5ms)
         ↓
7. Display in Streamlit (5-10ms)
         ↓
8. User Views Results
```

**Total Response Time: 20-125ms** ⚡

---

## Module Responsibilities

```
┌─────────────────────────────────────────────────────┐
│ app.py                                              │
│ - UI rendering                                      │
│ - User input handling                               │
│ - Results display                                   │
│ - Tab management                                    │
│ - CSV export                                        │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ nlp_processor.py                                    │
│ - Text tokenization                                 │
│ - Lemmatization                                     │
│ - Entity detection                                  │
│ - Intent recognition                                │
│ - Filter extraction                                 │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ sparql_generator.py                                 │
│ - Query pattern selection                           │
│ - SPARQL construction                               │
│ - Template management                               │
│ - Filter application                                │
│ - Aggregation handling                              │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ rdf_query_executor.py                               │
│ - RDF graph loading                                 │
│ - SPARQL execution                                  │
│ - Result extraction                                 │
│ - DataFrame conversion                              │
│ - Error handling                                    │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ config.py                                           │
│ - Configuration management                          │
│ - Default settings                                  │
│ - Vocabulary expansion                              │
│ - Feature toggles                                   │
└─────────────────────────────────────────────────────┘
```

---

## Error Handling Flow

```
User Query
    │
    ▼
┌─────────────┐
│ NLP Process │ ──Error──▶ Display Error Message
└─────┬───────┘
      │ Success
      ▼
┌─────────────┐
│ SPARQL Gen  │ ──Error──▶ Display Error Message
└─────┬───────┘
      │ Success
      ▼
┌─────────────┐
│ RDF Execute │ ──Error──▶ Display Error Message
└─────┬───────┘
      │ Success
      ▼
   Display Results
```

---

## Supported Query Patterns

```
Pattern 1: Simple List
  Input:  "List all [CLASS]"
  Output: SELECT ?var WHERE { ?x a cccm:[CLASS] }

Pattern 2: Filtered List
  Input:  "List [CLASS] in [LOCATION]"
  Output: SELECT ?var WHERE { ?x a cccm:[CLASS] ;
                               cccm:basedIn cccm:[LOCATION] }

Pattern 3: Aggregation
  Input:  "Count [CLASS]"
  Output: SELECT (COUNT(?x) AS ?total) WHERE { ?x a cccm:[CLASS] }

Pattern 4: Relationship
  Input:  "List [CLASS1] who [PROP] [CLASS2]"
  Output: SELECT ?var WHERE { ?x [PROP] ?y . ?y a cccm:[CLASS2] }

Pattern 5: Multi-Filter
  Input:  "List [STATUS] [CLASS] in [LOCATION]"
  Output: SELECT ?var WHERE { ?x a cccm:[CLASS] ;
                               cccm:basedIn cccm:[LOCATION] ;
                               cccm:hasStatus ?s .
                              ?s cccm:status "[STATUS]" }
```

---

This architecture provides:

- ✅ Clear separation of concerns
- ✅ Modular design
- ✅ Easy to extend
- ✅ Fast execution
- ✅ Comprehensive error handling
