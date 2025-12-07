# Natural Language to SPARQL Query Converter

A **Streamlit web application** that converts **Natural Language queries** into **SPARQL queries** and executes them on the **CCCM (Cross-Currency Credit Management) RDF dataset**.

This application uses **classical NLP techniques** (no LLMs) including:

- Tokenization
- Lemmatization
- Stopword removal
- POS tagging
- Rule-based entity and intent detection

## Features

✨ **Key Features:**

- 🎯 Natural language query input
- 🔤 Automatic SPARQL query generation
- 📊 Results displayed in interactive tables
- 🧠 NLP analysis visualization
- 📥 CSV export of results
- 🎨 Beautiful Streamlit UI
- 🚀 **Advanced pattern recognition** for complex queries:
  - Multiple entity aggregations (HAVING clauses)
  - Cross-border transaction detection
  - Percentage-based filtering
  - Comparison queries (banks vs fintechs)
  - Institution-specific filtering
  - Full money trail tracing
  - Numeric threshold comparisons

## Architecture

```
┌─────────────────┐
│  User Query     │
│  (Natural Lang) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  NLP Processor  │
│  - Tokenization │
│  - Lemmatization│
│  - Entity Det.  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ SPARQL Generator│
│  - Rule-based   │
│  - Templates    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  RDF Executor   │
│  - Query RDF    │
│  - Return Data  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Results Table  │
│  (Streamlit UI) │
└─────────────────┘
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup Steps

1. **Clone or navigate to the project directory:**

```bash
cd /home/waqardev/hammad-projects/nlp-implementation
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Download spaCy language model (if not auto-installed):**

```bash
python -m spacy download en_core_web_sm
```

## Usage

### Running the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

### Example Queries

Try these natural language queries:

#### Customer Queries

- "List all customers"
- "Show customers in India"
- "List customers living in India"
- "Show customers based in UK"
- "List customers in USA"

#### Institution Queries

- "List all banks"
- "Show institutions in India"
- "List all fintechs"
- "Show banks in UK"

#### Transaction Queries

- "List all transactions"
- "Show all remittances"
- "List customers who initiated transactions"
- "Show customers who initiated remittances"
- "List transactions and their processing institutions"

#### Status-based Queries

- "Show completed transactions"
- "List failed transactions"
- "Show pending remittances"

#### Aggregation Queries

- "Count customers"
- "Show customers with total number of accounts"
- "List customers with their accounts"

#### Complex Queries

**Basic Complex Queries:**

- "Show transactions from USD to INR"
- "List institutions based in India"

**Advanced Complex Queries:**

- "Show customers with multiple accounts" - Finds customers with more than one account
- "List remittances processed by fintech" - Filters remittances by FinTech institutions
- "Show cross-border transactions" - Detects currency conversion transactions
- "Compare banks versus fintechs" - Aggregates and compares transaction counts
- "Show transactions processed by ICICI" - Filters by specific institution name
- "Show customers who use both banks and fintechs" - Finds customers with both account types
- "Show full money trail" - Complete customer→account→institution→transaction chain
- "Show remittances over 200000" - Filters by amount threshold
- "Show top customer by transaction amount" - Ranks and returns highest
- "Show transactions with loss over 5%" - Calculates percentage loss
- "Show customers with foreign accounts" - Detects cross-border account ownership

## Project Structure

```
nlp-implementation/
│
├── app.py                      # Main Streamlit application
├── nlp_processor.py            # NLP processing module
├── sparql_generator.py         # SPARQL query generator
├── rdf_query_executor.py       # RDF query execution
├── requirements.txt            # Python dependencies
├── README.md                   # This file
│
└── CCCM PERFECTED.owl          # RDF dataset
```

## How It Works

### 1. NLP Processing (`nlp_processor.py`)

- **Tokenization**: Breaks query into words
- **Lemmatization**: Converts words to base form
- **Stopword Removal**: Removes common words
- **POS Tagging**: Identifies parts of speech
- **Entity Detection**: Maps tokens to RDF classes and properties
- **Intent Detection**: Determines query intent (list, count, filter)
- **Filter Extraction**: Detects conditions (country, status, etc.)

### 2. SPARQL Generation (`sparql_generator.py`)

- Analyzes NLP results
- Selects appropriate query template
- Constructs SPARQL query with:
  - Correct classes (Customer, Transaction, Bank, etc.)
  - Correct properties (fullName, basedIn, etc.)
  - Filters and conditions
  - Aggregations (COUNT, SUM, etc.)
  - Ordering (ASC, DESC)

### 3. Query Execution (`rdf_query_executor.py`)

- Loads RDF dataset using rdflib
- Executes SPARQL query
- Converts results to pandas DataFrame
- Handles errors gracefully

### 4. UI Display (`app.py`)

- Shows input box for queries
- Displays results in tables
- Shows generated SPARQL query
- Provides NLP analysis details
- Offers CSV download

## CCCM Dataset Schema

The RDF dataset includes:

**Classes:**

- `Customer`: People using the system
- `Transaction`: Money transfers
- `Remittance`: Specific type of transaction
- `Bank`: Banking institutions
- `FinTech`: Financial technology companies
- `Account`: Customer accounts
- `Currency`: Money currencies (USD, INR, etc.)
- `Country`: Countries (India, UK, USA, etc.)
- `Status`: Transaction status (Completed, Failed, Pending)
- `Rate`: Exchange rates

**Properties:**

- `fullName`: Customer name
- `basedIn`: Country location
- `hasAccount`: Customer's accounts
- `initiatedBy`: Transaction initiator
- `processedBy`: Institution processing transaction
- `amountSent`: Amount sent
- `amountReceived`: Amount received
- `fromCurrency`: Source currency
- `toCurrency`: Target currency
- `hasStatus`: Transaction status
- `bankName`: Institution name

## Example SPARQL Queries

### List all customers in India

```sparql
PREFIX cccm: <http://www.semanticweb.org/cccm#>
SELECT ?name
WHERE {
  ?cust a cccm:Customer ;
        cccm:fullName ?name ;
        cccm:basedIn cccm:India .
}
```

### List institutions based in India

```sparql
PREFIX cccm: <http://www.semanticweb.org/cccm#>
SELECT ?name
WHERE {
  ?i a ?type ;
     cccm:basedIn cccm:India ;
     cccm:bankName ?name .
  FILTER(?type IN (cccm:Bank, cccm:FinTech))
}
```

### Count accounts per customer

```sparql
PREFIX cccm: <http://www.semanticweb.org/cccm#>
SELECT ?custName (COUNT(?acc) AS ?NumAcc)
WHERE {
  ?cust a cccm:Customer ;
        cccm:fullName ?custName ;
        cccm:hasAccount ?acc .
}
GROUP BY ?custName
ORDER BY DESC(?NumAcc)
```

## Technologies Used

- **Streamlit**: Web application framework
- **spaCy**: NLP library for text processing
- **rdflib**: RDF graph manipulation and SPARQL querying
- **pandas**: Data manipulation and display
- **Python 3.8+**: Programming language

## NLP Techniques

This application uses **classical NLP techniques**:

1. **Tokenization**: Breaking text into words
2. **Lemmatization**: Converting words to base form (e.g., "customers" → "customer")
3. **Stopword Removal**: Removing common words (the, is, at, etc.)
4. **POS Tagging**: Identifying nouns, verbs, adjectives
5. **Rule-based Matching**: Mapping keywords to RDF entities
6. **Pattern Detection**: Finding filters and conditions
7. **Intent Recognition**: Understanding query purpose

**No LLMs or transformers are used** - only traditional NLP methods!

## Limitations

- **Fixed vocabulary**: Only recognizes predefined keywords
- **Simple queries**: Complex multi-clause queries may not work
- **No learning**: System doesn't improve from usage
- **English only**: Only supports English language
- **Pattern-based**: Relies on specific patterns and templates

## Future Enhancements

Possible improvements:

- [ ] Support for more complex queries
- [ ] Query history and favorites
- [ ] Visualization of results (charts, graphs)
- [ ] Query suggestions and auto-complete
- [ ] Support for INSERT/UPDATE/DELETE queries
- [ ] Multi-language support
- [ ] Custom dataset upload

## Troubleshooting

### spaCy model not found

```bash
python -m spacy download en_core_web_sm
```

### RDF file not found

Ensure `CCCM PERFECTED.owl` is in the same directory as `app.py`

### Import errors

```bash
pip install -r requirements.txt --upgrade
```

## License

This project is for educational purposes.

## Author

Created as a demonstration of classical NLP techniques for semantic query conversion.

---

**Happy Querying! 🚀**
