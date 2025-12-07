"""
Streamlit Web Application: Natural Language to SPARQL Query Converter
for CCCM (Cross-Currency Credit Management) RDF Dataset

This application converts natural language queries into SPARQL queries
and executes them on the CCCM RDF dataset using classical NLP techniques.
"""

import streamlit as st
import pandas as pd
from nlp_processor import NLPProcessor
from sparql_generator import SPARQLGenerator
from rdf_query_executor import RDFQueryExecutor
import os


hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Page configuration
st.set_page_config(
    page_title="NL to SPARQL Query Converter",
    page_icon="🔍",
    layout="wide"
)

# Initialize components
@st.cache_resource
def initialize_components():
    """Initialize NLP processor, SPARQL generator, and RDF executor"""
    nlp_processor = NLPProcessor()
    sparql_generator = SPARQLGenerator()
    
    # Get the path to the OWL file
    owl_file = "CCCM PERFECTED.owl"
    if not os.path.exists(owl_file):
        st.error(f"RDF dataset file '{owl_file}' not found!")
        return None, None, None
    
    rdf_executor = RDFQueryExecutor(owl_file)
    return nlp_processor, sparql_generator, rdf_executor

# Application header
st.title("🔍 Natural Language to SPARQL Query Converter")
st.markdown("""
Convert natural language queries into SPARQL and execute them on the **CCCM (Cross-Currency Credit Management)** RDF dataset.
This application uses **classical NLP techniques** (no LLMs) including tokenization, lemmatization, and rule-based entity detection.
""")

# Initialize components
nlp_processor, sparql_generator, rdf_executor = initialize_components()

if nlp_processor is None:
    st.stop()

# Sidebar with example queries
with st.sidebar:
    st.header("📚 Example Queries")
    st.markdown("""
    Try these example queries:
    
    **Customer Queries:**
    - List all customers
    - Show customers in India
    - List customers living in India
    - Show customers based in UK
    
    **Institution Queries:**
    - List all banks
    - Show institutions in India
    - List all fintechs
    
    **Transaction Queries:**
    - List all transactions
    - Show all remittances
    - List customers who initiated transactions
    - Show customers who initiated remittances
    
    **Account Queries:**
    - List customers with their accounts
    - Show customers with total number of accounts
    - Count accounts per customer
    
    **Complex Queries:**
    - List transactions and their processing institutions
    - Show completed transactions
    - List failed transactions
    - Show customers with multiple accounts
    - List remittances processed by fintech
    - Show cross-border transactions
    - Compare banks versus fintechs
    - Show transactions processed by ICICI
    - Show customers who use both banks and fintechs
    - Show full money trail
    - Show remittances over 200000
    - Show top customer by transaction amount
    """)
    
    st.markdown("---")
    st.markdown("**Dataset:** CCCM PERFECTED.owl")
    st.markdown("**Prefix:** `cccm: <http://www.semanticweb.org/cccm#>`")

# Main query interface
st.header("🎯 Enter Your Query")

# Input area
col1, col2 = st.columns([4, 1])

with col1:
    user_query = st.text_input(
        "Type your natural language query:",
        placeholder="e.g., List all customers in India",
        key="query_input"
    )

with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    submit_button = st.button("🔍 Convert & Execute", type="primary", use_container_width=True)

# Quick example buttons
st.markdown("**Quick Examples:**")
example_col1, example_col2, example_col3, example_col4 = st.columns(4)

with example_col1:
    if st.button("List all customers"):
        user_query = "List all customers"
        submit_button = True

with example_col2:
    if st.button("Customers in India"):
        user_query = "List all customers living in India"
        submit_button = True

with example_col3:
    if st.button("All institutions"):
        user_query = "List institutions based in India"
        submit_button = True

with example_col4:
    if st.button("All transactions"):
        user_query = "List all transactions"
        submit_button = True

# Process query
if submit_button and user_query:
    st.markdown("---")
    
    # Create tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Results", "🔤 SPARQL Query", "🧠 NLP Analysis", "📝 Query Info"])
    
    with st.spinner("Processing your query..."):
        try:
            # Step 1: NLP Processing
            nlp_result = nlp_processor.process(user_query)
            
            # Step 2: Generate SPARQL
            sparql_query = sparql_generator.generate(nlp_result)
            
            # Step 3: Execute SPARQL
            results_df, error = rdf_executor.execute(sparql_query)
            
            # Display results
            with tab1:
                st.subheader("Query Results")
                if error:
                    st.error(f"Error executing query: {error}")
                elif results_df is not None and not results_df.empty:
                    st.success(f"Found {len(results_df)} result(s)")
                    
                    # Display as table
                    st.dataframe(
                        results_df,
                        use_container_width=True,
                        hide_index=True
                    )
                    
                    # Download option
                    csv = results_df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Results as CSV",
                        data=csv,
                        file_name="query_results.csv",
                        mime="text/csv"
                    )
                else:
                    st.warning("No results found for your query.")
            
            with tab2:
                st.subheader("Generated SPARQL Query")
                st.code(sparql_query, language="sparql")
                
                # Copy button
                if st.button("📋 Copy SPARQL Query"):
                    st.code(sparql_query)
                    st.success("You can copy the query from the code block above!")
            
            with tab3:
                st.subheader("NLP Processing Analysis")
                
                # Original query
                st.markdown("**Original Query:**")
                st.info(user_query)
                
                # Detected entities
                col_a, col_b = st.columns(2)
                
                with col_a:
                    st.markdown("**Detected Classes:**")
                    if nlp_result.get('classes'):
                        for cls in nlp_result['classes']:
                            st.markdown(f"- `{cls}`")
                    else:
                        st.markdown("- None")
                    
                    st.markdown("**Detected Properties:**")
                    if nlp_result.get('properties'):
                        for prop in nlp_result['properties']:
                            st.markdown(f"- `{prop}`")
                    else:
                        st.markdown("- None")
                
                with col_b:
                    st.markdown("**Detected Intent:**")
                    st.markdown(f"- `{nlp_result.get('intent', 'unknown')}`")
                    
                    st.markdown("**Detected Filters:**")
                    if nlp_result.get('filters'):
                        for key, value in nlp_result['filters'].items():
                            st.markdown(f"- `{key}`: {value}")
                    else:
                        st.markdown("- None")
                
                # Tokens
                with st.expander("🔍 Token Analysis"):
                    st.markdown("**Tokens:**")
                    st.write(nlp_result.get('tokens', []))
                    
                    st.markdown("**Lemmas:**")
                    st.write(nlp_result.get('lemmas', []))
                    
                    if 'pos_tags' in nlp_result:
                        st.markdown("**POS Tags:**")
                        pos_df = pd.DataFrame({
                            'Token': nlp_result.get('tokens', []),
                            'POS': nlp_result.get('pos_tags', []),
                            'Lemma': nlp_result.get('lemmas', [])
                        })
                        st.dataframe(pos_df, use_container_width=True, hide_index=True)
            
            with tab4:
                st.subheader("Query Information")
                
                st.markdown("**Query Type:**")
                query_type = nlp_result.get('query_type', 'SELECT')
                st.badge(query_type)
                
                st.markdown("**Aggregation:**")
                if nlp_result.get('aggregation'):
                    st.markdown(f"- Type: `{nlp_result['aggregation'].get('type')}`")
                    st.markdown(f"- Variable: `{nlp_result['aggregation'].get('variable')}`")
                else:
                    st.markdown("- None")
                
                st.markdown("**Order By:**")
                if nlp_result.get('order_by'):
                    st.markdown(f"- Variable: `{nlp_result['order_by'].get('variable')}`")
                    st.markdown(f"- Direction: `{nlp_result['order_by'].get('direction')}`")
                else:
                    st.markdown("- None")
                
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.exception(e)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p><strong>NL to SPARQL Converter</strong> | Built with Streamlit & spaCy</p>
    <p>Using classical NLP techniques: Tokenization, Lemmatization, Rule-based Entity Detection</p>
</div>
""", unsafe_allow_html=True)
