# ORBITA
### Objective Reasoning And Bias Interpretation Tool for Analysis

An autonomous RAG-based multi-agent framework for cross-ideological argument mining and unbiased information synthesis.

---

## Project Structure
```
ORBITA/
├── modules/
│   ├── scraper.py        # News scraping via NewsAPI + Newspaper3k
│   ├── database.py       # ChromaDB ingestion + search
│   └── __init__.py
├── test.py               # Run scraper
├── database_test.py      # Run ChromaDB ingestion
├── Search_test.py        # Run search queries
├── .env                  # API keys (not pushed to GitHub)
└── requirements.txt
```

---

## Setup Instructions

### 1. Clone the repo
```
git clone https://github.com/Arsh-Vashist/ORBITA.git
cd ORBITA
```

### 2. Create and activate virtual environment
```
python -m venv venv
.\venv\Scripts\activate
```

### 3. Install dependencies
```
pip install -r requirements.txt
```

### 4. Create `.env` file in project root
```
NEWS_API_KEY=your_newsapi_key_here
GEMINI_API_KEY=your_gemini_key_here
```

---

## How to Run

### Step 1 — Scrape news articles
```
python test.py
```
Enter a topic (e.g. `MODI and Carney`), then enter a filename title. Saves articles as a JSON file.

### Step 2 — Ingest into ChromaDB
```
python database_test.py
```
Enter the JSON filename created in Step 1. Chunks and stores articles in ChromaDB.

### Step 3 — Search the database
```
python Search_test.py
```
Enter the collection name and type any query to retrieve relevant chunks.

---

## Tech Stack
- Python 3.12
- NewsAPI + Newspaper3k (scraping)
- ChromaDB (vector database)
- Sentence Transformers - all-MiniLM-L6-v2 (embeddings)
- Gemini API (coming soon - multi-agent system)
- LangChain (coming soon)
- Streamlit (coming soon)
```

Replace `Arsh-Vashist` with your GitHub username. Once done, run:
```
git add .
git commit -m "Initial commit - scraper, chromadb, search working"
git remote add origin https://github.com/YOUR_USERNAME/ORBITA.git
git push -u origin main