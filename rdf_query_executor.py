"""
RDF Query Executor Module

This module executes SPARQL queries on the RDF dataset and returns results.
"""

import rdflib
from rdflib import Graph
import pandas as pd
from typing import Tuple, Optional

class RDFQueryExecutor:
    """
    RDF Query Executor
    Loads RDF data and executes SPARQL queries
    """
    
    def __init__(self, rdf_file_path: str):
        """
        Initialize RDF graph from file
        
        Args:
            rdf_file_path: Path to the RDF/OWL file
        """
        self.graph = Graph()
        self.rdf_file_path = rdf_file_path
        
        # Load RDF data
        try:
            print(f"Loading RDF data from {rdf_file_path}...")
            self.graph.parse(rdf_file_path, format='xml')
            print(f"Loaded {len(self.graph)} triples from RDF dataset")
        except Exception as e:
            print(f"Error loading RDF file: {e}")
            raise
    
    def execute(self, sparql_query: str) -> Tuple[Optional[pd.DataFrame], Optional[str]]:
        """
        Execute SPARQL query on the RDF graph
        
        Args:
            sparql_query: SPARQL query string
            
        Returns:
            Tuple of (results DataFrame, error message)
        """
        try:
            # Execute query
            results = self.graph.query(sparql_query)
            
            # Convert results to pandas DataFrame
            if results:
                # Get variable names
                vars = results.vars
                
                # Extract data
                data = []
                for row in results:
                    row_data = []
                    for item in row:
                        if item is not None:
                            # Convert RDF terms to strings
                            row_data.append(str(item))
                        else:
                            row_data.append(None)
                    data.append(row_data)
                
                # Create DataFrame
                if data:
                    columns = [str(var) for var in vars] if vars else ['result']
                    df = pd.DataFrame(data, columns=columns)
                    return df, None
                else:
                    # Empty result set
                    columns = [str(var) for var in vars] if vars else ['result']
                    df = pd.DataFrame(columns=columns)
                    return df, None
            else:
                # No results
                return pd.DataFrame(), None
                
        except Exception as e:
            error_msg = f"Error executing SPARQL query: {str(e)}"
            print(error_msg)
            return None, error_msg
    
    def get_statistics(self) -> dict:
        """
        Get statistics about the RDF dataset
        
        Returns:
            Dictionary with dataset statistics
        """
        stats = {
            'total_triples': len(self.graph),
            'file_path': self.rdf_file_path,
        }
        
        # Count instances of each class
        class_query = """
        PREFIX cccm: <http://www.semanticweb.org/cccm#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        
        SELECT ?class (COUNT(?instance) AS ?count)
        WHERE {
          ?instance rdf:type ?class .
          FILTER(STRSTARTS(STR(?class), "http://www.semanticweb.org/cccm#"))
        }
        GROUP BY ?class
        ORDER BY DESC(?count)
        """
        
        try:
            results = self.graph.query(class_query)
            class_counts = {}
            for row in results:
                class_name = str(row[0]).split('#')[-1]
                count = int(row[1])
                class_counts[class_name] = count
            stats['class_counts'] = class_counts
        except Exception as e:
            print(f"Error getting class statistics: {e}")
            stats['class_counts'] = {}
        
        return stats
    
    def validate_query(self, sparql_query: str) -> Tuple[bool, Optional[str]]:
        """
        Validate SPARQL query syntax
        
        Args:
            sparql_query: SPARQL query string
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            # Try to parse the query
            self.graph.query(sparql_query)
            return True, None
        except Exception as e:
            return False, str(e)
    
    def get_all_classes(self) -> list:
        """
        Get all RDF classes in the dataset
        
        Returns:
            List of class names
        """
        query = """
        PREFIX cccm: <http://www.semanticweb.org/cccm#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        
        SELECT DISTINCT ?class
        WHERE {
          ?instance rdf:type ?class .
          FILTER(STRSTARTS(STR(?class), "http://www.semanticweb.org/cccm#"))
        }
        """
        
        try:
            results = self.graph.query(query)
            classes = [str(row[0]).split('#')[-1] for row in results]
            return sorted(classes)
        except Exception as e:
            print(f"Error getting classes: {e}")
            return []
    
    def get_all_properties(self) -> list:
        """
        Get all RDF properties in the dataset
        
        Returns:
            List of property names
        """
        query = """
        PREFIX cccm: <http://www.semanticweb.org/cccm#>
        
        SELECT DISTINCT ?property
        WHERE {
          ?subject ?property ?object .
          FILTER(STRSTARTS(STR(?property), "http://www.semanticweb.org/cccm#"))
        }
        """
        
        try:
            results = self.graph.query(query)
            properties = [str(row[0]).split('#')[-1] for row in results]
            return sorted(properties)
        except Exception as e:
            print(f"Error getting properties: {e}")
            return []
