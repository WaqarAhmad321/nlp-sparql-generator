"""
SPARQL Generator Module

This module generates SPARQL queries based on NLP analysis results.
Uses rule-based templates and dynamic query construction.
"""

from typing import Dict, List, Any

class SPARQLGenerator:
    """
    SPARQL Query Generator
    Converts structured NLP results into SPARQL queries
    """
    
    def __init__(self):
        """Initialize SPARQL generator with prefix"""
        self.prefix = "PREFIX cccm: <http://www.semanticweb.org/cccm#>\n"
        
    def generate(self, nlp_result: Dict[str, Any]) -> str:
        """
        Generate SPARQL query from NLP analysis result
        
        Args:
            nlp_result: Dictionary containing NLP analysis results
            
        Returns:
            SPARQL query string
        """
        classes = nlp_result.get('classes', [])
        properties = nlp_result.get('properties', [])
        filters = nlp_result.get('filters', {})
        aggregation = nlp_result.get('aggregation')
        order_by = nlp_result.get('order_by')
        intent = nlp_result.get('intent', 'list')
        special_pattern = nlp_result.get('special_pattern')
        comparison = nlp_result.get('comparison')
        specific_institution = nlp_result.get('specific_institution')
        
        # Handle special patterns first
        if special_pattern == 'HAVING_MULTIPLE':
            return self._generate_multiple_accounts_query()
        elif special_pattern == 'CROSS_BORDER':
            return self._generate_cross_border_query(classes)
        elif special_pattern == 'COMPARISON':
            return self._generate_comparison_query(classes, properties)
        elif special_pattern == 'FULL_CHAIN':
            return self._generate_full_chain_query()
        elif special_pattern == 'BOTH_TYPES':
            return self._generate_both_types_query()
        elif special_pattern == 'FOREIGN':
            return self._generate_foreign_accounts_query()
        elif special_pattern == 'LOSS_FILTER' or (comparison and comparison.get('type') == 'LOSS_PERCENTAGE'):
            return self._generate_loss_filter_query(comparison)
        elif special_pattern == 'TOP':
            return self._generate_top_query(classes, properties, aggregation)
        
        # Handle specific institution queries
        if specific_institution:
            return self._generate_specific_institution_query(classes, specific_institution)
        
        # Handle comparison filters
        if comparison and 'value' in comparison:
            return self._generate_comparison_filter_query(classes, comparison)
        
        # Determine query pattern based on detected entities
        if aggregation:
            return self._generate_aggregation_query(classes, properties, filters, 
                                                   aggregation, order_by)
        elif 'Transaction' in classes or 'Remittance' in classes:
            return self._generate_transaction_query(classes, properties, filters)
        elif 'Customer' in classes:
            return self._generate_customer_query(classes, properties, filters)
        elif 'Bank' in classes or 'FinTech' in classes or 'Institution' in classes:
            return self._generate_institution_query(classes, properties, filters)
        elif 'Account' in classes:
            return self._generate_account_query(classes, properties, filters)
        else:
            # Default: list all entities of detected class
            return self._generate_default_query(classes, properties, filters)
    
    def _generate_customer_query(self, classes: List[str], 
                                properties: List[str], 
                                filters: Dict[str, Any]) -> str:
        """Generate query for customer-related requests"""
        
        # Check if query is about international payments
        if 'basedIn' in filters and 'Currency' in classes and 'Transaction' in classes:
            country = filters['basedIn']
            query = f"""{self.prefix}
SELECT DISTINCT ?custName ?fromISO ?toISO
WHERE {{
  ?txn a cccm:Transaction ;
       cccm:fromCurrency ?fc ;
       cccm:toCurrency ?tc ;
       cccm:initiatedBy ?cust .
  ?cust cccm:basedIn cccm:{country} ;
        cccm:fullName ?custName .
  ?fc cccm:isoCode ?fromISO .
  ?tc cccm:isoCode ?toISO .
  FILTER(?fromISO != ?toISO)
}}"""
            return query
        
        # Check if we need to filter by country
        if 'basedIn' in filters:
            country = filters['basedIn']
            query = f"""{self.prefix}
SELECT ?name
WHERE {{
  ?cust a cccm:Customer ;
        cccm:fullName ?name ;
        cccm:basedIn cccm:{country} .
}}"""
        else:
            # List all customers
            query = f"""{self.prefix}
SELECT ?name
WHERE {{
  ?cust a cccm:Customer ;
        cccm:fullName ?name .
}}"""
        
        return query
    
    def _generate_institution_query(self, classes: List[str], 
                                   properties: List[str], 
                                   filters: Dict[str, Any]) -> str:
        """Generate query for institution-related requests"""
        
        # Determine institution types
        types = []
        if 'Bank' in classes:
            types.append('cccm:Bank')
        if 'FinTech' in classes:
            types.append('cccm:FinTech')
        if not types or 'Institution' in classes:
            types = ['cccm:Bank', 'cccm:FinTech']
        
        # Build query
        if 'basedIn' in filters:
            country = filters['basedIn']
            type_filter = f"FILTER(?type IN ({', '.join(types)}))" if len(types) > 1 else ""
            
            query = f"""{self.prefix}
SELECT ?name
WHERE {{
  ?i a ?type ;
     cccm:basedIn cccm:{country} ;
     cccm:bankName ?name .
  {type_filter}
}}"""
        else:
            if len(types) == 1:
                type_str = types[0]
                query = f"""{self.prefix}
SELECT ?name
WHERE {{
  ?i a {type_str} ;
     cccm:bankName ?name .
}}"""
            else:
                query = f"""{self.prefix}
SELECT ?name
WHERE {{
  ?i a ?type ;
     cccm:bankName ?name .
  FILTER(?type IN ({', '.join(types)}))
}}"""
        
        return query
    
    def _generate_transaction_query(self, classes: List[str], 
                                   properties: List[str], 
                                   filters: Dict[str, Any]) -> str:
        """Generate query for transaction-related requests"""
        
        # Check if it's remittances processed by FinTech only
        if 'Remittance' in classes and 'FinTech' in classes and 'processedBy' in properties:
            query = f"""{self.prefix}
SELECT (STRAFTER(STR(?r),"#") AS ?RemitID) ?custName ?amount ?fintechName
WHERE {{
  ?r a cccm:Remittance ;
     cccm:amountSent ?amount ;
     cccm:initiatedBy ?cust ;
     cccm:processedBy ?fintech .

  ?cust cccm:fullName ?custName .
  ?fintech a cccm:FinTech ;
           cccm:bankName ?fintechName .
}}
ORDER BY DESC(?amount)"""
            return query
        
        # Check if query is about customers who initiated transactions
        if 'initiatedBy' in properties or 'initiated' in properties or \
           any(prop in properties for prop in ['fullName']):
            
            if 'Remittance' in classes:
                # Customers who initiated remittances
                query = f"""{self.prefix}
SELECT DISTINCT ?custName
WHERE {{
  ?r a cccm:Remittance ;
     cccm:initiatedBy ?cust .
  ?cust cccm:fullName ?custName .
}}"""
            else:
                # Customers who initiated any transaction
                query = f"""{self.prefix}
SELECT DISTINCT ?custName
WHERE {{
  ?txn a cccm:Transaction ;
       cccm:initiatedBy ?cust .
  ?cust cccm:fullName ?custName .
}}"""
        
        # Check if query is about transactions and processing institutions
        elif 'processedBy' in properties or 'processed' in properties:
            query = f"""{self.prefix}
SELECT ?txnID ?instName
WHERE {{
  ?txn a cccm:Transaction ;
       cccm:processedBy ?inst .
  ?inst cccm:bankName ?instName .
  BIND(STRAFTER(STR(?txn), "#") AS ?txnID)
}}"""
        
        # Check for status filter
        elif 'status' in filters:
            status = filters['status']
            txn_class = 'cccm:Remittance' if 'Remittance' in classes else 'cccm:Transaction'
            query = f"""{self.prefix}
SELECT ?txnID ?amount ?status
WHERE {{
  ?txn a {txn_class} ;
       cccm:amountSent ?amount ;
       cccm:hasStatus ?s .
  ?s cccm:status ?status .
  FILTER(?status = "{status}")
  BIND(STRAFTER(STR(?txn), "#") AS ?txnID)
}}"""
        
        # Check for currency filter
        elif 'fromCurrency' in filters or 'toCurrency' in filters:
            from_curr = filters.get('fromCurrency', '')
            to_curr = filters.get('toCurrency', '')
            
            where_clauses = ["?txn a cccm:Transaction ;",
                           "     cccm:amountSent ?amount ."]
            
            if from_curr:
                where_clauses.append(f"  ?txn cccm:fromCurrency cccm:{from_curr} .")
            if to_curr:
                where_clauses.append(f"  ?txn cccm:toCurrency cccm:{to_curr} .")
            
            where_clause = "\n".join(where_clauses)
            
            query = f"""{self.prefix}
SELECT ?txnID ?amount
WHERE {{
  {where_clause}
  BIND(STRAFTER(STR(?txn), "#") AS ?txnID)
}}"""
        
        else:
            # List all transactions/remittances
            if 'Remittance' in classes:
                query = f"""{self.prefix}
SELECT ?txnID ?amount
WHERE {{
  ?txn a cccm:Remittance ;
       cccm:amountSent ?amount .
  BIND(STRAFTER(STR(?txn), "#") AS ?txnID)
}}"""
            else:
                query = f"""{self.prefix}
SELECT ?txnID ?amount
WHERE {{
  ?txn a cccm:Transaction ;
       cccm:amountSent ?amount .
  BIND(STRAFTER(STR(?txn), "#") AS ?txnID)
}}"""
        
        return query
    
    def _generate_account_query(self, classes: List[str], 
                               properties: List[str], 
                               filters: Dict[str, Any]) -> str:
        """Generate query for account-related requests"""
        
        # Simple account listing
        query = f"""{self.prefix}
SELECT ?custName ?accID
WHERE {{
  ?cust a cccm:Customer ;
        cccm:fullName ?custName ;
        cccm:hasAccount ?acc .
  BIND(STRAFTER(STR(?acc), "#") AS ?accID)
}}"""
        
        return query
    
    def _generate_aggregation_query(self, classes: List[str], 
                                   properties: List[str], 
                                   filters: Dict[str, Any],
                                   aggregation: Dict[str, str],
                                   order_by: Dict[str, str] = None) -> str:
        """Generate aggregation query (e.g., count accounts per customer)"""
        
        agg_type = aggregation.get('type', 'COUNT')
        agg_var = aggregation.get('variable', '?item')
        
        # For each bank, show total customers (complex aggregation)
        if 'Bank' in classes and 'Customer' in classes and 'serve' in properties:
            query = f"""{self.prefix}
SELECT ?bankName (COUNT(DISTINCT ?cust) AS ?NumCustomers)
WHERE {{
  ?acc a cccm:Account ;
       cccm:heldAt ?bank .
  ?bank a cccm:Bank ;
        cccm:bankName ?bankName .
  ?cust cccm:hasAccount ?acc .
}}
GROUP BY ?bankName
ORDER BY DESC(?NumCustomers)"""
            return query
        
        # Count accounts per customer
        if 'Account' in classes or 'hasAccount' in properties:
            query = f"""{self.prefix}
SELECT ?custName ({agg_type}({agg_var}) AS ?NumAcc)
WHERE {{
  ?cust a cccm:Customer ;
        cccm:fullName ?custName ;
        cccm:hasAccount {agg_var} .
}}
GROUP BY ?custName"""
            
            if order_by:
                direction = order_by.get('direction', 'DESC')
                query += f"\nORDER BY {direction}(?NumAcc)"
        
        # Count transactions by currency
        elif 'Currency' in classes and 'Transaction' in classes:
            query = f"""{self.prefix}
SELECT ?iso (COUNT(?txn) AS ?TxnCount)
WHERE {{
  ?txn cccm:fromCurrency ?cur .
  ?cur cccm:isoCode ?iso .
}}
GROUP BY ?iso
ORDER BY DESC(?TxnCount)"""
        
        # Count customers
        elif 'Customer' in classes and 'Transaction' not in classes:
            country_filter = ""
            if 'basedIn' in filters:
                country = filters['basedIn']
                country_filter = f"\n        cccm:basedIn cccm:{country} ;"
            
            query = f"""{self.prefix}
SELECT ({agg_type}(?cust) AS ?TotalCustomers)
WHERE {{
  ?cust a cccm:Customer ;{country_filter}
        cccm:fullName ?name .
}}"""
        
        # Count transactions
        elif 'Transaction' in classes:
            query = f"""{self.prefix}
SELECT ({agg_type}(?txn) AS ?TotalTransactions)
WHERE {{
  ?txn a cccm:Transaction .
}}"""
        
        else:
            # Generic count
            query = f"""{self.prefix}
SELECT ({agg_type}(?item) AS ?Total)
WHERE {{
  ?item a ?type .
}}"""
        
        return query
    
    def _generate_default_query(self, classes: List[str], 
                               properties: List[str], 
                               filters: Dict[str, Any]) -> str:
        """Generate default query when pattern is unclear"""
        
        if not classes:
            # No class detected, return all customers as default
            return f"""{self.prefix}
SELECT ?name
WHERE {{
  ?cust a cccm:Customer ;
        cccm:fullName ?name .
}}
LIMIT 10"""
        
        # Use first detected class
        class_name = classes[0]
        
        # Determine what property to select
        if class_name == 'Customer':
            prop = 'fullName'
            var = '?name'
        elif class_name in ['Bank', 'FinTech', 'Institution']:
            prop = 'bankName'
            var = '?name'
        elif class_name == 'Currency':
            prop = 'isoCode'
            var = '?code'
        elif class_name == 'Country':
            prop = 'countryName'
            var = '?name'
        else:
            # Generic
            var = '?value'
            query = f"""{self.prefix}
SELECT ?item
WHERE {{
  ?item a cccm:{class_name} .
}}
LIMIT 20"""
            return query
        
        query = f"""{self.prefix}
SELECT {var}
WHERE {{
  ?item a cccm:{class_name} ;
        cccm:{prop} {var} .
}}"""
        
        return query
    
    def _generate_multiple_accounts_query(self) -> str:
        """Generate query for customers with multiple accounts"""
        query = f"""{self.prefix}
SELECT ?custName (COUNT(?acc) AS ?NumAccounts)
WHERE {{
  ?cust a cccm:Customer ;
        cccm:fullName ?custName ;
        cccm:hasAccount ?acc .
}}
GROUP BY ?custName
HAVING(COUNT(?acc) > 1)
ORDER BY DESC(?NumAccounts)"""
        return query
    
    def _generate_cross_border_query(self, classes: List[str]) -> str:
        """Generate query for cross-border transactions (currency conversion)"""
        query = f"""{self.prefix}
SELECT ?TxnID ?custName ?fromISO ?toISO
WHERE {{
  ?txn a cccm:Transaction ;
       cccm:fromCurrency ?fc ;
       cccm:toCurrency ?tc ;
       cccm:initiatedBy ?cust .

  FILTER(?fc != ?tc)

  ?fc cccm:isoCode ?fromISO .
  ?tc cccm:isoCode ?toISO .
  ?cust cccm:fullName ?custName .

  BIND(STRAFTER(STR(?txn), "#") AS ?TxnID)
}}
ORDER BY ?custName"""
        return query
    
    def _generate_comparison_query(self, classes: List[str], properties: List[str]) -> str:
        """Generate comparison query (banks vs fintechs)"""
        query = f"""{self.prefix}
SELECT ?instName (COUNT(?txn) AS ?TotalTxns)
WHERE {{
  ?txn cccm:processedBy ?inst .
  ?inst cccm:bankName ?instName .
}}
GROUP BY ?instName
ORDER BY DESC(?TotalTxns)"""
        return query
    
    def _generate_full_chain_query(self) -> str:
        """Generate full money trail query"""
        query = f"""{self.prefix}
SELECT ?custName ?accID ?instName ?txnID ?amount
WHERE {{
  ?cust a cccm:Customer ;
        cccm:fullName ?custName ;
        cccm:hasAccount ?acc .

  ?acc cccm:heldAt ?inst .
  ?inst cccm:bankName ?instName .

  ?txn cccm:initiatedBy ?cust ;
       cccm:amountSent ?amount .

  BIND(STRAFTER(STR(?acc), "#") AS ?accID)
  BIND(STRAFTER(STR(?txn), "#") AS ?txnID)
}}
ORDER BY ?custName"""
        return query
    
    def _generate_both_types_query(self) -> str:
        """Generate query for customers using both banks and fintechs"""
        query = f"""{self.prefix}
SELECT DISTINCT ?custName
WHERE {{
  ?cust a cccm:Customer ;
        cccm:fullName ?custName ;
        cccm:hasAccount ?acc1, ?acc2 .

  ?acc1 cccm:heldAt ?inst1 .
  ?acc2 cccm:heldAt ?inst2 .

  ?inst1 a cccm:Bank .
  ?inst2 a cccm:FinTech .
}}"""
        return query
    
    def _generate_foreign_accounts_query(self) -> str:
        """Generate query for customers with foreign accounts"""
        query = f"""{self.prefix}
SELECT DISTINCT ?custName ?custCountry ?bankCountry
WHERE {{
  ?cust a cccm:Customer ;
        cccm:fullName ?custName ;
        cccm:basedIn ?cCountry ;
        cccm:hasAccount ?acc .

  ?cCountry cccm:countryName ?custCountry .

  ?acc cccm:heldAt ?inst .
  ?inst cccm:basedIn ?iCountry .
  ?iCountry cccm:countryName ?bankCountry .

  FILTER(?cCountry != ?iCountry)
}}"""
        return query
    
    def _generate_loss_filter_query(self, comparison: Dict[str, Any]) -> str:
        """Generate query for transactions with loss > threshold"""
        percentage = comparison.get('percentage', 5) if comparison else 5
        threshold = percentage / 100.0
        
        query = f"""{self.prefix}
SELECT ?TxnID ?custName ?sent ?received
WHERE {{
  ?txn a cccm:Transaction ;
       cccm:amountSent ?sent ;
       cccm:amountReceived ?received ;
       cccm:initiatedBy ?cust .

  FILTER((?sent - ?received) > (?sent * {threshold}))  
  BIND(STRAFTER(STR(?txn),"#") AS ?TxnID)
  ?cust cccm:fullName ?custName .
}}
ORDER BY DESC(?sent)"""
        return query
    
    def _generate_top_query(self, classes: List[str], properties: List[str], 
                           aggregation: Dict[str, str]) -> str:
        """Generate query for top customer/institution by some metric"""
        
        if 'Customer' in classes and 'Transaction' in classes:
            # Customer with highest transaction amount
            query = f"""{self.prefix}
SELECT ?custName (SUM(?amount) AS ?TotalSent)
WHERE {{
  ?txn a cccm:Transaction ;
       cccm:amountSent ?amount ;
       cccm:initiatedBy ?cust .
  ?cust cccm:fullName ?custName .
}}
GROUP BY ?custName
ORDER BY DESC(?TotalSent)
LIMIT 1"""
        elif 'FinTech' in classes and 'Remittance' in classes:
            # FinTech with most remittances
            query = f"""{self.prefix}
SELECT ?fintechName (COUNT(?r) AS ?NumRemittances)
WHERE {{
  ?r a cccm:Remittance ;
     cccm:processedBy ?fintech .

  ?fintech a cccm:FinTech ;
           cccm:bankName ?fintechName .
}}
GROUP BY ?fintechName
ORDER BY DESC(?NumRemittances)"""
        elif 'Rate' in classes or 'exchange' in properties:
            # Highest exchange rates
            query = f"""{self.prefix}
SELECT ?rateID ?value ?src ?tgt
WHERE {{
  ?r a cccm:Rate ;
     cccm:rateValue ?value ;
     cccm:rateSource ?s ;
     cccm:rateTarget ?t .
  ?s cccm:isoCode ?src .
  ?t cccm:isoCode ?tgt .

  BIND(STRAFTER(STR(?r),"#") AS ?rateID)
}}
ORDER BY DESC(?value)
LIMIT 10"""
        else:
            # Default top query
            query = self._generate_aggregation_query(classes, properties, {}, 
                                                     aggregation or {'type': 'COUNT', 'variable': '?item'}, 
                                                     {'variable': '?total', 'direction': 'DESC'})
        
        return query
    
    def _generate_specific_institution_query(self, classes: List[str], 
                                            institution: str) -> str:
        """Generate query for specific institution"""
        query = f"""{self.prefix}
SELECT ?TxnID ?custName ?amount
WHERE {{
  ?txn cccm:processedBy cccm:{institution} ;
       cccm:amountSent ?amount ;
       cccm:initiatedBy ?cust .

  ?cust cccm:fullName ?custName .
  BIND(STRAFTER(STR(?txn),"#") AS ?TxnID)
}}
ORDER BY DESC(?amount)"""
        return query
    
    def _generate_comparison_filter_query(self, classes: List[str], 
                                         comparison: Dict[str, Any]) -> str:
        """Generate query with numeric comparison filter"""
        operator = comparison.get('operator', '>')
        value = comparison.get('value', 0)
        
        if 'Remittance' in classes:
            query = f"""{self.prefix}
SELECT ?custName ?amount
WHERE {{
  ?r a cccm:Remittance ;
     cccm:amountSent ?amount ;
     cccm:initiatedBy ?cust .
  FILTER(?amount {operator} {value})

  ?cust cccm:fullName ?custName .
}}
ORDER BY DESC(?amount)"""
        else:
            query = f"""{self.prefix}
SELECT ?TxnID ?amount
WHERE {{
  ?txn a cccm:Transaction ;
       cccm:amountSent ?amount .
  FILTER(?amount {operator} {value})
  
  BIND(STRAFTER(STR(?txn),"#") AS ?TxnID)
}}
ORDER BY DESC(?amount)"""
        
        return query
