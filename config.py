"""
Configuration file for NL to SPARQL Converter

Modify these settings to customize the application behavior.
"""

# RDF Dataset Configuration
RDF_DATASET = {
    'file_path': 'CCCM PERFECTED.owl',
    'format': 'xml',  # Format: 'xml', 'turtle', 'n3', 'nt'
    'namespace': 'http://www.semanticweb.org/cccm#',
    'prefix': 'cccm'
}

# Streamlit UI Configuration
UI_CONFIG = {
    'page_title': 'NL to SPARQL Query Converter',
    'page_icon': '🔍',
    'layout': 'wide',  # 'wide' or 'centered'
    'theme': 'light',  # 'light' or 'dark'
}

# NLP Configuration
NLP_CONFIG = {
    'model': 'en_core_web_sm',  # spaCy model to use
    'remove_stopwords': True,
    'lemmatize': True,
    'pos_tagging': True,
}

# Query Configuration
QUERY_CONFIG = {
    'default_limit': 100,  # Default LIMIT for queries
    'enable_aggregation': True,
    'enable_ordering': True,
    'enable_filtering': True,
}

# Display Configuration
DISPLAY_CONFIG = {
    'show_nlp_analysis': True,
    'show_sparql_query': True,
    'show_query_info': True,
    'enable_csv_download': True,
    'max_results_display': 1000,
}

# Example Queries (shown in sidebar)
EXAMPLE_QUERIES = [
    "List all customers",
    "Show customers in India",
    "List all banks",
    "Show institutions in India",
    "List all transactions",
    "Show all remittances",
    "List customers who initiated transactions",
    "Show customers with total number of accounts",
    "List failed transactions",
    "Show completed remittances",
]

# Vocabulary Expansion
# Add custom class mappings here
CUSTOM_CLASS_MAPPINGS = {
    # 'keyword': 'RDFClass'
    # Example:
    # 'client': 'Customer',
    # 'wallet': 'Account',
}

# Add custom property mappings here
CUSTOM_PROPERTY_MAPPINGS = {
    # 'keyword': 'rdfProperty'
    # Example:
    # 'title': 'fullName',
    # 'country': 'basedIn',
}

# Add custom country mappings here
CUSTOM_COUNTRY_MAPPINGS = {
    # 'keyword': 'Country'
    # Example:
    # 'pak': 'Pakistan',
    # 'aus': 'Australia',
}

# Debug Configuration
DEBUG_CONFIG = {
    'verbose_logging': False,
    'print_nlp_results': False,
    'print_sparql_queries': False,
    'show_error_traces': True,
}

# Cache Configuration
CACHE_CONFIG = {
    'enable_caching': True,
    'cache_ttl': 3600,  # Time to live in seconds
}
