"""
Test Script for NL to SPARQL Converter

This script tests the NLP processor and SPARQL generator
with example queries without running the full Streamlit app.
"""

from nlp_processor import NLPProcessor
from sparql_generator import SPARQLGenerator
import json

def test_query(query: str, processor: NLPProcessor, generator: SPARQLGenerator):
    """Test a single query"""
    print(f"\n{'='*80}")
    print(f"QUERY: {query}")
    print(f"{'='*80}")
    
    # Process with NLP
    nlp_result = processor.process(query)
    
    # Display NLP analysis
    print("\n--- NLP Analysis ---")
    print(f"Intent: {nlp_result.get('intent')}")
    print(f"Classes: {nlp_result.get('classes')}")
    print(f"Properties: {nlp_result.get('properties')}")
    print(f"Filters: {nlp_result.get('filters')}")
    print(f"Aggregation: {nlp_result.get('aggregation')}")
    print(f"Tokens: {nlp_result.get('tokens')}")
    print(f"Lemmas: {nlp_result.get('lemmas')}")
    
    # Generate SPARQL
    sparql_query = generator.generate(nlp_result)
    
    print("\n--- Generated SPARQL ---")
    print(sparql_query)
    print()

def main():
    """Main test function"""
    print("="*80)
    print("Testing NL to SPARQL Converter")
    print("="*80)
    
    # Initialize components
    print("\nInitializing NLP Processor...")
    processor = NLPProcessor()
    
    print("Initializing SPARQL Generator...")
    generator = SPARQLGenerator()
    
    # Test queries
    test_queries = [
        # Customer queries
        "List all customers",
        "Show customers in India",
        "List customers living in UK",
        "Show customers based in USA",
        
        # Institution queries
        "List all banks",
        "Show institutions in India",
        "List all fintechs",
        
        # Transaction queries
        "List all transactions",
        "Show all remittances",
        "List customers who initiated transactions",
        "Show customers who initiated remittances",
        "List transactions and their processing institutions",
        
        # Status queries
        "Show completed transactions",
        "List failed transactions",
        
        # Aggregation queries
        "Count customers",
        "Show customers with total number of accounts",
        "List customers with their accounts",
        
        # Complex queries
        "List institutions based in India",
    ]
    
    print(f"\nTesting {len(test_queries)} queries...\n")
    
    for query in test_queries:
        try:
            test_query(query, processor, generator)
        except Exception as e:
            print(f"ERROR: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*80)
    print("Testing Complete!")
    print("="*80)

if __name__ == "__main__":
    main()
