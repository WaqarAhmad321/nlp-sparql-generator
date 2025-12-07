# Complex Queries Guide

This guide explains the advanced query capabilities added to the NL-to-SPARQL converter system.

## Overview

The system now supports **20+ complex SPARQL query patterns** using classical NLP techniques. These patterns go beyond basic entity retrieval to include:

- Aggregations with HAVING clauses
- Cross-border transaction detection
- Percentage-based calculations
- Comparison queries
- Institution-specific filtering
- Full entity chain traversal
- Numeric threshold filtering

## Special Pattern Detection

The NLP processor now detects the following special patterns:

### 1. HAVING_MULTIPLE

**Trigger Words:** "multiple", "more than one", "having multiple"

**Example Query:** "Show customers with multiple accounts"

**Generated SPARQL:**

```sparql
SELECT ?customer (COUNT(?account) AS ?accountCount)
WHERE {
    ?customer a cccm:Customer .
    ?customer cccm:hasAccount ?account .
}
GROUP BY ?customer
HAVING(COUNT(?account) > 1)
```

### 2. CROSS_BORDER

**Trigger Words:** "cross-border", "cross border", "currency conversion"

**Example Query:** "Show cross-border transactions"

**Generated SPARQL:**

```sparql
SELECT ?transaction ?fromCurrency ?toCurrency
WHERE {
    ?transaction a cccm:Transaction .
    ?transaction cccm:fromCurrency ?fromCurrency .
    ?transaction cccm:toCurrency ?toCurrency .
    FILTER(?fromCurrency != ?toCurrency)
}
```

### 3. COMPARISON

**Trigger Words:** "compare", "versus", "vs", "banks versus fintechs"

**Example Query:** "Compare banks versus fintechs"

**Generated SPARQL:**

```sparql
SELECT ?institutionType (COUNT(?transaction) AS ?transactionCount)
WHERE {
    ?transaction a cccm:Transaction .
    ?transaction cccm:processedBy ?institution .
    ?institution a ?institutionType .
    FILTER(?institutionType = cccm:Bank || ?institutionType = cccm:FinTech)
}
GROUP BY ?institutionType
```

### 4. BOTH_TYPES

**Trigger Words:** "both banks and fintechs", "both types"

**Example Query:** "Show customers who use both banks and fintechs"

**Generated SPARQL:**

```sparql
SELECT ?customer
WHERE {
    ?customer cccm:hasAccount ?bankAccount .
    ?bankAccount cccm:maintainedBy ?bank .
    ?bank a cccm:Bank .

    ?customer cccm:hasAccount ?fintechAccount .
    ?fintechAccount cccm:maintainedBy ?fintech .
    ?fintech a cccm:FinTech .

    FILTER(?bank != ?fintech)
}
```

### 5. FULL_CHAIN

**Trigger Words:** "full trail", "money trail", "complete chain", "end-to-end"

**Example Query:** "Show full money trail"

**Generated SPARQL:**

```sparql
SELECT ?customer ?account ?institution ?transaction
WHERE {
    ?customer a cccm:Customer .
    ?customer cccm:hasAccount ?account .
    ?account cccm:maintainedBy ?institution .
    ?transaction cccm:fromAccount ?account .
}
```

### 6. FOREIGN_ACCOUNTS

**Trigger Words:** "foreign accounts", "accounts abroad", "international accounts"

**Example Query:** "Show customers with foreign accounts"

**Generated SPARQL:**

```sparql
SELECT ?customer ?account ?institution
WHERE {
    ?customer a cccm:Customer .
    ?customer cccm:basedIn ?customerCountry .
    ?customer cccm:hasAccount ?account .
    ?account cccm:maintainedBy ?institution .
    ?institution cccm:basedIn ?institutionCountry .
    FILTER(?customerCountry != ?institutionCountry)
}
```

### 7. LOSS_FILTER

**Trigger Words:** "loss", "transaction loss", "with loss over X%"

**Example Query:** "Show transactions with loss over 5%"

**Generated SPARQL:**

```sparql
SELECT ?transaction ?amountSent ?amountReceived
       ((?amountSent - ?amountReceived) AS ?loss)
       (((?amountSent - ?amountReceived) / ?amountSent * 100) AS ?lossPercentage)
WHERE {
    ?transaction a cccm:Transaction .
    ?transaction cccm:amountSent ?amountSent .
    ?transaction cccm:amountReceived ?amountReceived .
    FILTER((?amountSent - ?amountReceived) > (?amountSent * 0.05))
}
```

### 8. TOP_ENTITY

**Trigger Words:** "top customer", "highest", "maximum"

**Example Query:** "Show top customer by transaction amount"

**Generated SPARQL:**

```sparql
SELECT ?customer (SUM(?amount) AS ?totalAmount)
WHERE {
    ?customer a cccm:Customer .
    ?customer cccm:hasAccount ?account .
    ?transaction cccm:fromAccount ?account .
    ?transaction cccm:amountSent ?amount .
}
GROUP BY ?customer
ORDER BY DESC(?totalAmount)
LIMIT 1
```

## Comparison Detection

The system detects numeric comparisons and operators:

### Supported Operators

- **Greater than:** `>`, "greater than", "more than", "above", "over"
- **Less than:** `<`, "less than", "below", "under"
- **Equal:** `=`, "equal to", "exactly"

### Example Queries

1. **"Show remittances over 200000"**

   - Detects: operator `>`, amount `200000`
   - Generates: `FILTER(?amount > 200000)`

2. **"List transactions below 100000"**

   - Detects: operator `<`, amount `100000`
   - Generates: `FILTER(?amount < 100000)`

3. **"Show transactions equal to 500000"**
   - Detects: operator `=`, amount `500000`
   - Generates: `FILTER(?amount = 500000)`

## Institution-Specific Filtering

The system recognizes specific institution names:

### Supported Institutions

**Banks:**

- ICICI (ICICI_Bank)
- HDFC (HDFC_Bank)
- SBI (State_Bank_of_India)
- Axis (Axis_Bank)
- Barclays

**FinTechs:**

- Wise
- Revolut
- PayPal
- Stripe

### Example Query

**"Show transactions processed by ICICI"**

Generated SPARQL:

```sparql
SELECT ?transaction
WHERE {
    ?transaction a cccm:Transaction .
    ?transaction cccm:processedBy cccm:ICICI_Bank .
}
```

## Query Type Enhancements

### Enhanced Transaction Queries

**FinTech-processed Remittances:**

Query: "List remittances processed by fintech"

```sparql
SELECT ?remittance ?fintech
WHERE {
    ?remittance a cccm:Remittance .
    ?remittance cccm:processedBy ?fintech .
    ?fintech a cccm:FinTech .
}
```

### Enhanced Aggregation Queries

**Bank Customer Counts:**

Query: "Count customers per bank"

```sparql
SELECT ?bank (COUNT(DISTINCT ?customer) AS ?customerCount)
WHERE {
    ?customer cccm:hasAccount ?account .
    ?account cccm:maintainedBy ?bank .
    ?bank a cccm:Bank .
}
GROUP BY ?bank
```

**Currency Counts:**

Query: "Count transactions per currency"

```sparql
SELECT ?currency (COUNT(?transaction) AS ?count)
WHERE {
    ?transaction cccm:fromCurrency ?currency .
}
GROUP BY ?currency
```

### Enhanced Customer Queries

**International Payments:**

Query: "Show customers who made international payments"

```sparql
SELECT DISTINCT ?customer
WHERE {
    ?customer cccm:hasAccount ?account .
    ?transaction cccm:fromAccount ?account .
    ?transaction cccm:fromCurrency ?fromCurr .
    ?transaction cccm:toCurrency ?toCurr .
    FILTER(?fromCurr != ?toCurr)
}
```

## Testing Your Queries

To test these complex queries:

1. **Start the application:**

   ```bash
   streamlit run app.py
   ```

2. **Try these test queries:**

   - ✅ "Show customers with multiple accounts"
   - ✅ "List remittances processed by fintech"
   - ✅ "Show cross-border transactions"
   - ✅ "Compare banks versus fintechs"
   - ✅ "Show transactions processed by ICICI"
   - ✅ "Show customers who use both banks and fintechs"
   - ✅ "Show full money trail"
   - ✅ "Show transactions with loss over 5%"
   - ✅ "Show remittances over 200000"
   - ✅ "Show top customer by transaction amount"
   - ✅ "Show customers with foreign accounts"

3. **Check the tabs:**
   - **Results Tab:** View the query results
   - **SPARQL Tab:** See the generated SPARQL query
   - **NLP Analysis Tab:** Understand how the query was parsed

## Implementation Details

### Files Modified

1. **nlp_processor.py** (~450 lines)

   - Added `comparison_keywords` dictionary
   - Added `special_patterns` dictionary
   - Added `_detect_special_pattern()` method
   - Added `_detect_comparison()` method
   - Added `_detect_specific_institution()` method

2. **sparql_generator.py** (~650 lines)

   - Modified `generate()` method for special pattern routing
   - Added 10+ new query generator methods:
     - `_generate_multiple_accounts_query()`
     - `_generate_cross_border_query()`
     - `_generate_comparison_query()`
     - `_generate_full_chain_query()`
     - `_generate_both_types_query()`
     - `_generate_foreign_accounts_query()`
     - `_generate_loss_filter_query()`
     - `_generate_top_query()`
     - `_generate_specific_institution_query()`
     - `_generate_comparison_filter_query()`
   - Enhanced existing methods:
     - `_generate_transaction_query()` for FinTech remittances
     - `_generate_aggregation_query()` for bank/currency counts
     - `_generate_customer_query()` for international payments

3. **EXAMPLES.md** (~750 lines)

   - Added 11 new complex query examples (queries 20-30)
   - Documented all special patterns with SPARQL

4. **README.md** (~360 lines)
   - Added advanced pattern recognition features
   - Added complex query examples section

## Architecture

```
User Query
    ↓
┌─────────────────────────┐
│   NLP Processor         │
│  ├─ Tokenization        │
│  ├─ Entity Detection    │
│  ├─ Intent Detection    │
│  ├─ Pattern Detection   │  ← NEW
│  ├─ Comparison Detection│  ← NEW
│  └─ Institution Mapping │  ← NEW
└─────────┬───────────────┘
          ↓
┌─────────────────────────┐
│  SPARQL Generator       │
│  ├─ Basic Queries       │
│  ├─ Special Patterns    │  ← NEW
│  ├─ Comparison Filters  │  ← NEW
│  └─ Complex Chains      │  ← NEW
└─────────┬───────────────┘
          ↓
┌─────────────────────────┐
│  RDF Query Executor     │
│  └─ Execute & Return    │
└─────────────────────────┘
```

## Troubleshooting

### Query Not Working?

1. **Check NLP Analysis Tab:** See how your query was parsed
2. **Check SPARQL Tab:** Verify the generated SPARQL is correct
3. **Try variations:** Use different keywords from the pattern triggers

### Common Issues

**Issue:** "Show customers with multiple accounts" returns nothing

- **Solution:** Check if your RDF dataset has customers with >1 account

**Issue:** "Compare banks versus fintechs" shows only one type

- **Solution:** Verify your dataset has both Bank and FinTech entities

**Issue:** Specific institution name not recognized

- **Solution:** Add it to `institution_mapping` in `nlp_processor.py`

## Future Enhancements

Potential additions for even more complex queries:

1. **Time-based filtering:** "transactions in last 30 days"
2. **Geographic aggregations:** "total remittances per country"
3. **Multi-level grouping:** "customers grouped by country and bank"
4. **Nested comparisons:** "banks with more customers than average"
5. **Path finding:** "shortest route from customer to transaction"

## Contributing

To add new query patterns:

1. Add pattern keywords to `special_patterns` in `nlp_processor.py`
2. Update `_detect_special_pattern()` method
3. Create new generator method in `sparql_generator.py`
4. Add routing in `generate()` method
5. Document in EXAMPLES.md
6. Test thoroughly!

---

**Built with ❤️ using Classical NLP (No LLMs)**
