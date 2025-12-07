"""
NLP Processor Module

This module handles natural language processing using classical NLP techniques:
- Tokenization
- Lemmatization
- Stopword removal
- POS tagging
- Rule-based entity and intent detection
"""

import spacy
import re
from typing import Dict, List, Any

class NLPProcessor:
    """
    NLP Processor for converting natural language to structured data
    using classical NLP techniques (no LLMs)
    """
    
    def __init__(self):
        """Initialize spaCy model and define RDF mappings"""
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("Downloading spaCy model 'en_core_web_sm'...")
            import subprocess
            subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
            self.nlp = spacy.load("en_core_web_sm")
        
        # RDF Class mappings (keywords -> RDF classes)
        self.class_mappings = {
            'customer': 'Customer',
            'customers': 'Customer',
            'people': 'Customer',
            'person': 'Customer',
            'user': 'Customer',
            'users': 'Customer',
            
            'transaction': 'Transaction',
            'transactions': 'Transaction',
            'txn': 'Transaction',
            'transfer': 'Transaction',
            'transfers': 'Transaction',
            
            'remittance': 'Remittance',
            'remittances': 'Remittance',
            'remit': 'Remittance',
            
            'account': 'Account',
            'accounts': 'Account',
            'acc': 'Account',
            
            'bank': 'Bank',
            'banks': 'Bank',
            
            'fintech': 'FinTech',
            'fintechs': 'FinTech',
            
            'institution': 'Institution',
            'institutions': 'Institution',
            
            'currency': 'Currency',
            'currencies': 'Currency',
            
            'country': 'Country',
            'countries': 'Country',
            
            'rate': 'Rate',
            'rates': 'Rate',
            'exchange': 'Rate',
            
            'status': 'Status',
        }
        
        # RDF Property mappings (keywords -> RDF properties)
        self.property_mappings = {
            'name': 'fullName',
            'names': 'fullName',
            'fullname': 'fullName',
            'full': 'fullName',
            
            'country': 'basedIn',
            'location': 'basedIn',
            'based': 'basedIn',
            'living': 'basedIn',
            'live': 'basedIn',
            'from': 'basedIn',
            
            'amount': 'amountSent',
            'sent': 'amountSent',
            'send': 'amountSent',
            
            'received': 'amountReceived',
            'receive': 'amountReceived',
            
            'initiated': 'initiatedBy',
            'initiate': 'initiatedBy',
            'sender': 'initiatedBy',
            
            'processed': 'processedBy',
            'process': 'processedBy',
            'processor': 'processedBy',
            
            'account': 'hasAccount',
            'accounts': 'hasAccount',
            
            'balance': 'balance',
            
            'status': 'hasStatus',
            'state': 'hasStatus',
            
            'bankname': 'bankName',
            
            'currency': 'fromCurrency',
            'fromcurrency': 'fromCurrency',
            'tocurrency': 'toCurrency',
            
            'rate': 'appliedRate',
        }
        
        # Country mappings
        self.countries = {
            'india': 'India',
            'indian': 'India',
            'uk': 'UK',
            'britain': 'UK',
            'england': 'UK',
            'usa': 'USA',
            'america': 'USA',
            'us': 'USA',
            'united states': 'USA',
        }
        
        # Status mappings
        self.statuses = {
            'completed': 'Completed',
            'complete': 'Completed',
            'success': 'Completed',
            'successful': 'Completed',
            'pending': 'Pending',
            'failed': 'Failed',
            'failure': 'Failed',
            'fail': 'Failed',
        }
        
        # Intent keywords
        self.intent_keywords = {
            'list': 'list',
            'show': 'list',
            'display': 'list',
            'get': 'list',
            'retrieve': 'list',
            'find': 'list',
            'fetch': 'list',
            
            'count': 'count',
            'number': 'count',
            'total': 'count',
            'how many': 'count',
            
            'filter': 'filter',
            'where': 'filter',
            'with': 'filter',
        }
        
        # Aggregation keywords
        self.aggregation_keywords = {
            'count': 'COUNT',
            'total': 'COUNT',
            'number': 'COUNT',
            'sum': 'SUM',
            'average': 'AVG',
            'avg': 'AVG',
            'minimum': 'MIN',
            'min': 'MIN',
            'maximum': 'MAX',
            'max': 'MAX',
            'highest': 'MAX',
            'lowest': 'MIN',
        }
        
        # Comparison keywords
        self.comparison_keywords = {
            'greater': '>',
            'more': '>',
            'over': '>',
            'above': '>',
            'less': '<',
            'under': '<',
            'below': '<',
            'equal': '=',
            'equals': '=',
        }
        
        # Special query patterns
        self.special_patterns = {
            'multiple': 'HAVING_MULTIPLE',
            'both': 'BOTH_TYPES',
            'cross-border': 'CROSS_BORDER',
            'international': 'CROSS_BORDER',
            'foreign': 'FOREIGN',
            'highest': 'TOP',
            'top': 'TOP',
            'most': 'TOP',
            'trail': 'FULL_CHAIN',
            'chain': 'FULL_CHAIN',
            'compare': 'COMPARISON',
            'versus': 'COMPARISON',
            'vs': 'COMPARISON',
        }
        
    def process(self, query: str) -> Dict[str, Any]:
        """
        Process natural language query and extract structured information
        
        Args:
            query: Natural language query string
            
        Returns:
            Dictionary containing extracted entities and intent
        """
        # Convert to lowercase for processing
        query_lower = query.lower()
        
        # Process with spaCy
        doc = self.nlp(query_lower)
        
        # Extract tokens and lemmas
        tokens = [token.text for token in doc if not token.is_punct]
        lemmas = [token.lemma_ for token in doc if not token.is_punct]
        pos_tags = [token.pos_ for token in doc if not token.is_punct]
        
        # Remove stopwords for better analysis
        filtered_tokens = [token.text for token in doc 
                          if not token.is_stop and not token.is_punct]
        
        # Detect intent
        intent = self._detect_intent(tokens, lemmas)
        
        # Detect classes
        classes = self._detect_classes(tokens, lemmas)
        
        # Detect properties
        properties = self._detect_properties(tokens, lemmas)
        
        # Detect filters (conditions)
        filters = self._detect_filters(query_lower, tokens, lemmas, doc)
        
        # Detect aggregation
        aggregation = self._detect_aggregation(tokens, lemmas)
        
        # Detect ordering
        order_by = self._detect_ordering(tokens, lemmas)
        
        # Detect special patterns
        special_pattern = self._detect_special_pattern(tokens, lemmas, query_lower)
        
        # Detect comparison filters
        comparison = self._detect_comparison(tokens, lemmas, query_lower)
        
        # Detect specific institutions
        specific_institution = self._detect_specific_institution(query_lower)
        
        # Determine query type
        query_type = 'SELECT'
        if aggregation:
            query_type = 'SELECT_AGGREGATION'
        if special_pattern:
            query_type = f'SELECT_{special_pattern}'
        
        result = {
            'original_query': query,
            'tokens': tokens,
            'lemmas': lemmas,
            'pos_tags': pos_tags,
            'filtered_tokens': filtered_tokens,
            'intent': intent,
            'classes': classes,
            'properties': properties,
            'filters': filters,
            'aggregation': aggregation,
            'order_by': order_by,
            'query_type': query_type,
            'special_pattern': special_pattern,
            'comparison': comparison,
            'specific_institution': specific_institution,
        }
        
        return result
    
    def _detect_intent(self, tokens: List[str], lemmas: List[str]) -> str:
        """Detect the intent of the query"""
        for token in tokens + lemmas:
            if token in self.intent_keywords:
                return self.intent_keywords[token]
        return 'list'
    
    def _detect_classes(self, tokens: List[str], lemmas: List[str]) -> List[str]:
        """Detect RDF classes mentioned in the query"""
        classes = set()
        
        for token in tokens + lemmas:
            if token in self.class_mappings:
                classes.add(self.class_mappings[token])
        
        return list(classes)
    
    def _detect_properties(self, tokens: List[str], lemmas: List[str]) -> List[str]:
        """Detect RDF properties mentioned in the query"""
        properties = set()
        
        for token in tokens + lemmas:
            if token in self.property_mappings:
                properties.add(self.property_mappings[token])
        
        return list(properties)
    
    def _detect_filters(self, query: str, tokens: List[str], 
                       lemmas: List[str], doc) -> Dict[str, Any]:
        """Detect filter conditions in the query"""
        filters = {}
        
        # Detect country filters
        for token in tokens + lemmas:
            if token in self.countries:
                filters['basedIn'] = self.countries[token]
                break
        
        # Detect status filters
        for token in tokens + lemmas:
            if token in self.statuses:
                filters['status'] = self.statuses[token]
                break
        
        # Detect numeric filters (e.g., "aged 21", "with 3 credits")
        for i, token in enumerate(doc):
            if token.like_num:
                # Look at surrounding context
                if i > 0:
                    prev_token = doc[i-1].text.lower()
                    if prev_token in ['age', 'aged', 'years']:
                        filters['age'] = int(token.text)
                    elif prev_token in ['credit', 'credits']:
                        filters['credits'] = int(token.text)
                    elif prev_token in ['balance']:
                        filters['balance'] = float(token.text)
        
        # Detect currency filters (e.g., "from USD to INR")
        currencies = ['usd', 'inr', 'gbp', 'eur', 'jpy', 'aud']
        for curr in currencies:
            if curr in query:
                if 'from' in query:
                    filters['fromCurrency'] = curr.upper()
                if 'to' in query and query.index('to') > query.index(curr):
                    filters['toCurrency'] = curr.upper()
        
        # Detect specific entity mentions (e.g., "enrolled in Data Structures")
        # Look for preposition + capitalized words
        for i, token in enumerate(doc):
            if token.text in ['in', 'at', 'with', 'for'] and i < len(doc) - 1:
                next_token = doc[i+1]
                if next_token.pos_ == 'PROPN' or next_token.is_title:
                    # Capture multi-word proper nouns
                    entity_words = [next_token.text]
                    j = i + 2
                    while j < len(doc) and (doc[j].pos_ == 'PROPN' or doc[j].is_title):
                        entity_words.append(doc[j].text)
                        j += 1
                    filters['entity_name'] = ' '.join(entity_words)
        
        return filters
    
    def _detect_aggregation(self, tokens: List[str], 
                           lemmas: List[str]) -> Dict[str, str]:
        """Detect aggregation functions in the query"""
        for token in tokens + lemmas:
            if token in self.aggregation_keywords:
                return {
                    'type': self.aggregation_keywords[token],
                    'variable': '?acc' if 'account' in tokens + lemmas else '?item'
                }
        
        # Check for phrases like "total number of"
        query_str = ' '.join(tokens)
        if 'total' in query_str and 'number' in query_str:
            return {
                'type': 'COUNT',
                'variable': '?acc' if 'account' in tokens + lemmas else '?item'
            }
        
        return None
    
    def _detect_ordering(self, tokens: List[str], 
                        lemmas: List[str]) -> Dict[str, str]:
        """Detect ORDER BY clauses"""
        order_keywords = ['order', 'sort', 'arrange']
        direction_keywords = {
            'ascending': 'ASC',
            'asc': 'ASC',
            'descending': 'DESC',
            'desc': 'DESC',
        }
        
        has_order = any(keyword in tokens + lemmas for keyword in order_keywords)
        
        if has_order or 'desc' in tokens + lemmas:
            direction = 'DESC' if 'desc' in tokens + lemmas else 'ASC'
            return {
                'variable': '?NumAcc',
                'direction': direction
            }
        
        return None
    
    def _detect_special_pattern(self, tokens: List[str], 
                                lemmas: List[str], query: str) -> str:
        """Detect special query patterns"""
        for token in tokens + lemmas:
            if token in self.special_patterns:
                return self.special_patterns[token]
        
        # Pattern-based detection
        if 'multiple' in query and 'account' in query:
            return 'HAVING_MULTIPLE'
        if ('cross' in query and 'border' in query) or 'currency conversion' in query:
            return 'CROSS_BORDER'
        if 'compare' in query or 'vs' in query or 'versus' in query:
            return 'COMPARISON'
        if 'trail' in query or 'chain' in query or 'linked' in query:
            return 'FULL_CHAIN'
        if 'both' in query and ('bank' in query or 'fintech' in query):
            return 'BOTH_TYPES'
        if 'foreign' in query or 'different country' in query:
            return 'FOREIGN'
        if 'lost' in query or 'loss' in query:
            return 'LOSS_FILTER'
        
        return None
    
    def _detect_comparison(self, tokens: List[str], 
                          lemmas: List[str], query: str) -> Dict[str, Any]:
        """Detect comparison operations"""
        comparison = {}
        
        # Check for percentage filters
        if '%' in query or 'percent' in query:
            # Extract percentage value
            import re
            match = re.search(r'(\d+)\s*%', query)
            if match:
                comparison['percentage'] = int(match.group(1))
                
                # Check what it's comparing
                if 'lost' in query or 'loss' in query:
                    comparison['type'] = 'LOSS_PERCENTAGE'
        
        # Check for numeric comparisons
        for i, token in enumerate(tokens):
            if token in self.comparison_keywords:
                comparison['operator'] = self.comparison_keywords[token]
                
                # Look for numeric value nearby
                if i + 1 < len(tokens):
                    next_token = tokens[i + 1]
                    if next_token.replace(',', '').replace('.', '').isdigit():
                        comparison['value'] = float(next_token.replace(',', ''))
        
        return comparison if comparison else None
    
    def _detect_specific_institution(self, query: str) -> str:
        """Detect specific institution names in the query"""
        institutions = {
            'icici': 'ICICI_Bank',
            'hdfc': 'HDFC',
            'axis': 'Axis_Bank',
            'kotak': 'Kotak_Bank',
            'wise': 'Wise',
            'paytm': 'Paytm',
            'phonepe': 'PhonePe',
            'razorpay': 'Razorpay',
            'barclays': 'Barclays',
            'chase': 'Chase',
        }
        
        for keyword, inst_name in institutions.items():
            if keyword in query:
                return inst_name
        
        return None
