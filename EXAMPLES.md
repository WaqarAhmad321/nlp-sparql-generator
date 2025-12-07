# Example Queries for NL to SPARQL Converter

This document contains example natural language queries and their corresponding SPARQL queries for the CCCM dataset.

---

## Customer Queries

### 1. List all customers

**Natural Language:** "List all customers"

**Generated SPARQL:**

```sparql
PREFIX cccm: <http://www.semanticweb.org/cccm#>
SELECT ?name
WHERE {
  ?cust a cccm:Customer ;
        cccm:fullName ?name .
}
```

---

### 2. List all customers living in India

**Natural Language:** "List all customers living in India"

**Generated SPARQL:**

```sparql
PREFIX cccm: <http://www.semanticweb.org/cccm#>
SELECT ?name
WHERE {
  ?cust a cccm:Customer ;
        cccm:fullName ?name ;
        cccm:basedIn cccm:India .
}
```

**Description:** Filters customers based on country.

---

### 3. Show customers in UK

**Natural Language:** "Show customers in UK"

**Generated SPARQL:**

```sparql
PREFIX cccm: <http://www.semanticweb.org/cccm#>
SELECT ?name
WHERE {
  ?cust a cccm:Customer ;
        cccm:fullName ?name ;
        cccm:basedIn cccm:UK .
}
```

---

### 4. List customers in USA

**Natural Language:** "List customers in USA"

**Generated SPARQL:**

```sparql
PREFIX cccm: <http://www.semanticweb.org/cccm#>
SELECT ?name
WHERE {
  ?cust a cccm:Customer ;
        cccm:fullName ?name ;
        cccm:basedIn cccm:USA .
}
```

---

## Institution Queries

### 5. List all banks

**Natural Language:** "List all banks"

**Generated SPARQL:**

```sparql
PREFIX cccm: <http://www.semanticweb.org/cccm#>
SELECT ?name
WHERE {
  ?i a cccm:Bank ;
     cccm:bankName ?name .
}
```

---

### 6. List institutions based in India

**Natural Language:** "List institutions based in India"

**Generated SPARQL:**

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

**Description:** Shows all banks and fintechs based in India.

---

### 7. List all fintechs

**Natural Language:** "List all fintechs"

**Generated SPARQL:**

```sparql
PREFIX cccm: <http://www.semanticweb.org/cccm#>
SELECT ?name
WHERE {
  ?i a cccm:FinTech ;
     cccm:bankName ?name .
}
```

---

## Transaction Queries

### 8. List all transactions

**Natural Language:** "List all transactions"

**Generated SPARQL:**

```sparql
PREFIX cccm: <http://www.semanticweb.org/cccm#>
SELECT ?txnID ?amount
WHERE {
  ?txn a cccm:Transaction ;
       cccm:amountSent ?amount .
  BIND(STRAFTER(STR(?txn), "#") AS ?txnID)
}
```

---

### 9. Show all remittances

**Natural Language:** "Show all remittances"

**Generated SPARQL:**

```sparql
PREFIX cccm: <http://www.semanticweb.org/cccm#>
SELECT ?txnID ?amount
WHERE {
  ?txn a cccm:Remittance ;
       cccm:amountSent ?amount .
  BIND(STRAFTER(STR(?txn), "#") AS ?txnID)
}
```

---

### 10. List customers who initiated any transaction

**Natural Language:** "List customers who initiated any transaction"

**Generated SPARQL:**

```sparql
PREFIX cccm: <http://www.semanticweb.org/cccm#>
SELECT DISTINCT ?custName
WHERE {
  ?txn a cccm:Transaction ;
       cccm:initiatedBy ?cust .
  ?cust cccm:fullName ?custName .
}
```

**Description:** Shows customers involved in sending money.

---

### 11. List customers who initiated remittances

**Natural Language:** "List customers who initiated remittances"

**Generated SPARQL:**

```sparql
PREFIX cccm: <http://www.semanticweb.org/cccm#>
SELECT DISTINCT ?custName
WHERE {
  ?r a cccm:Remittance ;
     cccm:initiatedBy ?cust .
  ?cust cccm:fullName ?custName .
}
```

**Description:** Shows customers involved in remittance transfers.

---

### 12. List transactions and their processing institutions

**Natural Language:** "List transactions and their processing institutions"

**Generated SPARQL:**

```sparql
PREFIX cccm: <http://www.semanticweb.org/cccm#>
SELECT ?txnID ?instName
WHERE {
  ?txn a cccm:Transaction ;
       cccm:processedBy ?inst .
  ?inst cccm:bankName ?instName .
  BIND(STRAFTER(STR(?txn), "#") AS ?txnID)
}
```

**Description:** Retrieves transactions with the processing institution name.

---

## Account Queries

### 13. List customers with their accounts

**Natural Language:** "List customers with their accounts"

**Generated SPARQL:**

```sparql
PREFIX cccm: <http://www.semanticweb.org/cccm#>
SELECT ?custName ?accID
WHERE {
  ?cust a cccm:Customer ;
        cccm:fullName ?custName ;
        cccm:hasAccount ?acc .
  BIND(STRAFTER(STR(?acc), "#") AS ?accID)
}
```

---

### 14. List customers along with their total number of accounts

**Natural Language:** "Show customers with total number of accounts"

**Generated SPARQL:**

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

**Description:** Counts accounts owned by each customer.

---

## Status-Based Queries

### 15. Show completed transactions

**Natural Language:** "Show completed transactions"

**Generated SPARQL:**

```sparql
PREFIX cccm: <http://www.semanticweb.org/cccm#>
SELECT ?txnID ?amount ?status
WHERE {
  ?txn a cccm:Transaction ;
       cccm:amountSent ?amount ;
       cccm:hasStatus ?s .
  ?s cccm:status ?status .
  FILTER(?status = "Completed")
  BIND(STRAFTER(STR(?txn), "#") AS ?txnID)
}
```

---

### 16. List failed transactions

**Natural Language:** "List failed transactions"

**Generated SPARQL:**

```sparql
PREFIX cccm: <http://www.semanticweb.org/cccm#>
SELECT ?txnID ?amount ?status
WHERE {
  ?txn a cccm:Transaction ;
       cccm:amountSent ?amount ;
       cccm:hasStatus ?s .
  ?s cccm:status ?status .
  FILTER(?status = "Failed")
  BIND(STRAFTER(STR(?txn), "#") AS ?txnID)
}
```

---

### 17. Show pending remittances

**Natural Language:** "Show pending remittances"

**Generated SPARQL:**

```sparql
PREFIX cccm: <http://www.semanticweb.org/cccm#>
SELECT ?txnID ?amount ?status
WHERE {
  ?txn a cccm:Remittance ;
       cccm:amountSent ?amount ;
       cccm:hasStatus ?s .
  ?s cccm:status ?status .
  FILTER(?status = "Pending")
  BIND(STRAFTER(STR(?txn), "#") AS ?txnID)
}
```

---

## Aggregation Queries

### 18. Count customers

**Natural Language:** "Count customers"

**Generated SPARQL:**

```sparql
PREFIX cccm: <http://www.semanticweb.org/cccm#>
SELECT (COUNT(?cust) AS ?TotalCustomers)
WHERE {
  ?cust a cccm:Customer ;
        cccm:fullName ?name .
}
```

---

### 19. Count transactions

**Natural Language:** "Count transactions"

**Generated SPARQL:**

```sparql
PREFIX cccm: <http://www.semanticweb.org/cccm#>
SELECT (COUNT(?txn) AS ?TotalTransactions)
WHERE {
  ?txn a cccm:Transaction .
}
```

---

## Testing Your Queries

You can test these queries in three ways:

### 1. Through Streamlit App

```bash
streamlit run app.py
```

Type any query in the text box and click "Convert & Execute"

### 2. Through Test Script

```bash
python3 test_queries.py
```

This will test all predefined queries without the UI

### 3. Direct SPARQL Execution

Use any SPARQL endpoint or RDF tool to execute the queries directly on the `CCCM PERFECTED.owl` file.

---

## Query Patterns

The system recognizes these patterns:

### Pattern 1: Simple List

- "List all [CLASS]"
- "Show [CLASS]"
- "Get [CLASS]"

### Pattern 2: Filtered List

- "List [CLASS] in [COUNTRY]"
- "Show [CLASS] based in [LOCATION]"
- "Get [CLASS] from [PLACE]"

### Pattern 3: Relationship Queries

- "List [CLASS] who [PROPERTY] [CLASS]"
- "Show [CLASS] and their [PROPERTY]"

### Pattern 4: Aggregation

- "Count [CLASS]"
- "Total number of [CLASS]"
- "[CLASS] with number of [PROPERTY]"

### Pattern 5: Status Filtering

- "Show [STATUS] [CLASS]"
- "List [CLASS] that are [STATUS]"

---

## Vocabulary

### Supported Classes

- Customer, customers, people, person, user, users
- Transaction, transactions, transfer, transfers
- Remittance, remittances
- Account, accounts
- Bank, banks
- FinTech, fintechs
- Institution, institutions
- Currency, currencies
- Country, countries

### Supported Properties

- name, fullname
- country, location, based, living
- amount, sent, received
- initiated, sender
- processed, processor
- account, accounts
- balance
- status, state

### Supported Countries

- India, UK, USA, Britain, England, America

### Supported Status Values

- Completed, Pending, Failed

---

## Tips for Best Results

1. **Use simple, direct language**

   - ✅ "List all customers"
   - ❌ "I would like to see a comprehensive list of all the customers"

2. **Include the class name**

   - ✅ "Show customers in India"
   - ❌ "Show those in India"

3. **Use recognized keywords**

   - ✅ "List institutions based in India"
   - ❌ "List organizations located in India"

4. **Be specific about filters**

   - ✅ "Show completed transactions"
   - ❌ "Show successful ones"

5. **For aggregations, use clear terms**
   - ✅ "Count customers"
   - ✅ "Total number of accounts"
   - ❌ "How many are there"

---

## Limitations

The system currently does **NOT** support:

- ❌ Complex multi-clause queries with AND/OR
- ❌ Nested queries with multiple levels
- ❌ Queries requiring inference or reasoning
- ❌ Update/Insert/Delete operations
- ❌ Mathematical operations beyond COUNT
- ❌ Date/time filtering
- ❌ String pattern matching (REGEX)
- ❌ Optional clauses (OPTIONAL)
- ❌ Union queries (UNION)

These limitations exist because the system uses **rule-based NLP** without machine learning models.

---

## Complex Queries

### 20. Customers with multiple accounts

**Natural Language:** "Show customers with multiple accounts"

**Generated SPARQL:**

```sparql
PREFIX cccm: <http://www.semanticweb.org/cccm#>
SELECT ?custName (COUNT(?acc) AS ?NumAccounts)
WHERE {
  ?cust a cccm:Customer ;
        cccm:fullName ?custName ;
        cccm:hasAccount ?acc .
}
GROUP BY ?custName
HAVING(COUNT(?acc) > 1)
ORDER BY DESC(?NumAccounts)
```

**Description:** Finds customers that have more than one account.

---

### 21. Remittances processed by FinTech only

**Natural Language:** "List remittances processed by fintech"

**Generated SPARQL:**

```sparql
PREFIX cccm: <http://www.semanticweb.org/cccm#>
SELECT (STRAFTER(STR(?r),"#") AS ?RemitID) ?custName ?amount ?fintechName
WHERE {
  ?r a cccm:Remittance ;
     cccm:amountSent ?amount ;
     cccm:initiatedBy ?cust ;
     cccm:processedBy ?fintech .

  ?cust cccm:fullName ?custName .
  ?fintech a cccm:FinTech ;
           cccm:bankName ?fintechName .
}
ORDER BY DESC(?amount)
```

---

### 22. Cross-border transactions (currency conversion)

**Natural Language:** "Show cross-border transactions"

**Generated SPARQL:**

```sparql
PREFIX cccm: <http://www.semanticweb.org/cccm#>
SELECT ?TxnID ?custName ?fromISO ?toISO
WHERE {
  ?txn a cccm:Transaction ;
       cccm:fromCurrency ?fc ;
       cccm:toCurrency ?tc ;
       cccm:initiatedBy ?cust .

  FILTER(?fc != ?tc)

  ?fc cccm:isoCode ?fromISO .
  ?tc cccm:isoCode ?toISO .
  ?cust cccm:fullName ?custName .

  BIND(STRAFTER(STR(?txn), "#") AS ?TxnID)
}
ORDER BY ?custName
```

---

### 23. Transactions processed by ICICI Bank

**Natural Language:** "Show transactions processed by ICICI"

**Generated SPARQL:**

```sparql
PREFIX cccm: <http://www.semanticweb.org/cccm#>
SELECT ?TxnID ?custName ?amount
WHERE {
  ?txn cccm:processedBy cccm:ICICI_Bank ;
       cccm:amountSent ?amount ;
       cccm:initiatedBy ?cust .

  ?cust cccm:fullName ?custName .
  BIND(STRAFTER(STR(?txn),"#") AS ?TxnID)
}
ORDER BY DESC(?amount)
```

---

### 24. Customers using both banks and fintechs

**Natural Language:** "Show customers who use both banks and fintechs"

**Generated SPARQL:**

```sparql
PREFIX cccm: <http://www.semanticweb.org/cccm#>
SELECT DISTINCT ?custName
WHERE {
  ?cust a cccm:Customer ;
        cccm:fullName ?custName ;
        cccm:hasAccount ?acc1, ?acc2 .

  ?acc1 cccm:heldAt ?inst1 .
  ?acc2 cccm:heldAt ?inst2 .

  ?inst1 a cccm:Bank .
  ?inst2 a cccm:FinTech .
}
```

---

### 25. Full money trail (customer → account → institution → transaction)

**Natural Language:** "Show full money trail"

**Generated SPARQL:**

```sparql
PREFIX cccm: <http://www.semanticweb.org/cccm#>
SELECT ?custName ?accID ?instName ?txnID ?amount
WHERE {
  ?cust a cccm:Customer ;
        cccm:fullName ?custName ;
        cccm:hasAccount ?acc .

  ?acc cccm:heldAt ?inst .
  ?inst cccm:bankName ?instName .

  ?txn cccm:initiatedBy ?cust ;
       cccm:amountSent ?amount .

  BIND(STRAFTER(STR(?acc), "#") AS ?accID)
  BIND(STRAFTER(STR(?txn), "#") AS ?txnID)
}
ORDER BY ?custName
```

---

### 26. Transactions with money lost > 5%

**Natural Language:** "Show transactions with loss over 5%"

**Generated SPARQL:**

```sparql
PREFIX cccm: <http://www.semanticweb.org/cccm#>
SELECT ?TxnID ?custName ?sent ?received
WHERE {
  ?txn a cccm:Transaction ;
       cccm:amountSent ?sent ;
       cccm:amountReceived ?received ;
       cccm:initiatedBy ?cust .

  FILTER((?sent - ?received) > (?sent * 0.05))
  BIND(STRAFTER(STR(?txn),"#") AS ?TxnID)
  ?cust cccm:fullName ?custName .
}
ORDER BY DESC(?sent)
```

---

### 27. Compare banks vs fintechs by transaction volume

**Natural Language:** "Compare banks versus fintechs"

**Generated SPARQL:**

```sparql
PREFIX cccm: <http://www.semanticweb.org/cccm#>
SELECT ?instName (COUNT(?txn) AS ?TotalTxns)
WHERE {
  ?txn cccm:processedBy ?inst .
  ?inst cccm:bankName ?instName .
}
GROUP BY ?instName
ORDER BY DESC(?TotalTxns)
```

---

### 28. Customers with foreign accounts

**Natural Language:** "Show customers with foreign accounts"

**Generated SPARQL:**

```sparql
PREFIX cccm: <http://www.semanticweb.org/cccm#>
SELECT DISTINCT ?custName ?custCountry ?bankCountry
WHERE {
  ?cust a cccm:Customer ;
        cccm:fullName ?custName ;
        cccm:basedIn ?cCountry ;
        cccm:hasAccount ?acc .

  ?cCountry cccm:countryName ?custCountry .

  ?acc cccm:heldAt ?inst .
  ?inst cccm:basedIn ?iCountry .
  ?iCountry cccm:countryName ?bankCountry .

  FILTER(?cCountry != ?iCountry)
}
```

---

### 29. Customer with highest total transaction amount

**Natural Language:** "Show top customer by transaction amount"

**Generated SPARQL:**

```sparql
PREFIX cccm: <http://www.semanticweb.org/cccm#>
SELECT ?custName (SUM(?amount) AS ?TotalSent)
WHERE {
  ?txn a cccm:Transaction ;
       cccm:amountSent ?amount ;
       cccm:initiatedBy ?cust .
  ?cust cccm:fullName ?custName .
}
GROUP BY ?custName
ORDER BY DESC(?TotalSent)
LIMIT 1
```

---

### 30. Remittances over 200,000

**Natural Language:** "Show remittances over 200000"

**Generated SPARQL:**

```sparql
PREFIX cccm: <http://www.semanticweb.org/cccm#>
SELECT ?custName ?amount
WHERE {
  ?r a cccm:Remittance ;
     cccm:amountSent ?amount ;
     cccm:initiatedBy ?cust .
  FILTER(?amount > 200000)

  ?cust cccm:fullName ?custName .
}
ORDER BY DESC(?amount)
```

---

**For more information, see the main README.md file.**
