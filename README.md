# ORBITA: Objective Reasoning and Bias Interpretation Tool

ORBITA is a news analysis framework designed to detect and deconstruct media bias. Unlike standard news aggregators, it uses a Multi-Agent RAG (Retrieval-Augmented Generation) system to mine arguments from different ideological perspectives and synthesize an unbiased report.

The project was developed to address the problem of "echo chambers" by ensuring that the AI analyzes an equal distribution of supportive and critical viewpoints before reaching a conclusion.

## Core Features

* **Smart Query Expansion:** Uses spaCy NER to break down a user topic into multiple search queries for better coverage.
* **Automated Stance Balancing:** Filters and balances the dataset to ensure a 50/50 split between different perspectives before ingestion.
* **Multi-Agent Synthesis:** Uses a three-agent system (Analyst, Critic, and Arbitrator) to cross-reference facts and identify sensationalism.
* **Bias Analytics:** Provides visual tools like a Stance Meter and Bias Radar to quantify the lean of the analyzed articles.
* **Hallucination Check:** Compares AI-generated scores with mathematical VADER sentiment scores to ensure reliability.

## Project Structure

```
ORBITA/
├── modules/
│   ├── agent_analyst.py     # Handles supportive argument mining
│   ├── agent_critic.py      # Handles critical/opposing argument mining
│   ├── agent_arbitrator.py   # Final synthesis with Chain-of-Thought
│   ├── intent_decoder.py     # spaCy-based query processing
│   ├── stance_filter.py      # Rebalances dataset (Pro/Against)
│   ├── deduplicator.py       # Removes duplicate news entries
│   ├── scraper.py            # NewsAPI and Newspaper4k integration
│   ├── database.py           # ChromaDB management
│   ├── nlp_analyzer.py       # Independent VADER/spaCy validation
│   └── visualizer.py         # Plotly dashboard components
├── app.py                    # Streamlit dashboard
├── .env                      # API keys (Protected)
└── requirements.txt          # Dependencies
```

## Setup and Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Arsh-Vashist/ORBITA.git
cd ORBITA
```

### 2. Environment Setup
```bash
python -m venv venv
# Activate venv (Windows)
.\venv\Scripts\activate
# Activate venv (Mac/Linux)
source venv/bin/activate

pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 3. API Configuration
Create a `.env` file in the root directory and add your keys:
```env
NEWS_API_KEY=your_newsapi_key_here
GEMINI_API_KEY=your_gemini_key_here
```

## Usage

To launch the dashboard, run:
```bash
streamlit run app.py
```

1.  **Scrape & Ingest:** Enter a topic in the sidebar. The system will fetch articles, deduplicate them, and store them in ChromaDB.
2.  **Analyze:** The engine overview will show the mathematical sentiment and top entities.
3.  **Synthesis:** The multi-agent section will display the breakdown of arguments from both sides along with a final unbiased verdict.

## Tech Stack

* **Frontend:** Streamlit
* **LLM:** Google Gemini Pro
* **Database:** ChromaDB (Vector Store)
* **NLP:** spaCy, VADER
* **Data:** NewsAPI, Newspaper4k
