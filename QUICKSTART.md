# Quick Start Guide

Get your NL to SPARQL converter running in 3 simple steps!

## 🚀 Quick Start

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

Or use the installation script:

```bash
chmod +x install.sh
./install.sh
```

### Step 2: Run the Application

```bash
streamlit run app.py
```

### Step 3: Try a Query

Once the app opens in your browser (http://localhost:8501), try:

```
List all customers in India
```

That's it! 🎉

---

## 📋 System Requirements

- Python 3.8 or higher
- 500 MB free disk space
- Internet connection (for first-time installation)

---

## 🧪 Quick Test (Without UI)

Want to test without running the full Streamlit app?

```bash
python3 test_queries.py
```

This will run 20+ example queries and show the generated SPARQL for each.

---

## 📚 Example Queries to Try

### Basic Queries

```
List all customers
Show all banks
List all transactions
```

### Filtered Queries

```
List customers in India
Show institutions in UK
List failed transactions
```

### Complex Queries

```
Show customers with total number of accounts
List customers who initiated remittances
List transactions and their processing institutions
```

---

## 🆘 Troubleshooting

### Problem: "spaCy model not found"

**Solution:**

```bash
python3 -m spacy download en_core_web_sm
```

### Problem: "File not found: CCCM PERFECTED.owl"

**Solution:** Make sure the OWL file is in the same directory as app.py

### Problem: "Module not found"

**Solution:** Install requirements again:

```bash
pip install -r requirements.txt --upgrade
```

### Problem: "Port already in use"

**Solution:** Run on a different port:

```bash
streamlit run app.py --server.port 8502
```

---

## 🎯 What to Expect

When you run the app, you'll see:

1. **Input Box**: Type your natural language query
2. **Results Tab**: See query results in a table
3. **SPARQL Tab**: View the generated SPARQL query
4. **NLP Analysis Tab**: See how the query was parsed
5. **Query Info Tab**: View additional query details

---

## 📖 More Information

- Full documentation: See `README.md`
- Example queries: See `EXAMPLES.md`
- Architecture details: See code comments in each module

---

## 🎨 Features You'll Love

✅ Instant query conversion
✅ Interactive results table
✅ CSV export functionality
✅ Beautiful UI with Streamlit
✅ Detailed NLP analysis
✅ No coding required!

---

## 🔧 Advanced Usage

### Custom Configuration

Edit `app.py` to:

- Change the RDF dataset file
- Modify UI appearance
- Add custom query templates

### Extending Vocabulary

Edit `nlp_processor.py` to:

- Add new class mappings
- Add new property mappings
- Support new entities

### Custom SPARQL Templates

Edit `sparql_generator.py` to:

- Add new query patterns
- Support complex queries
- Customize output format

---

## 🤝 Need Help?

Check these resources:

1. **Example Queries**: EXAMPLES.md
2. **Full Documentation**: README.md
3. **Test Script**: test_queries.py
4. **Code Comments**: Each .py file has detailed comments

---

**Happy Querying! 🚀**

Now go ahead and try: `streamlit run app.py`
