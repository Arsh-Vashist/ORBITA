import streamlit as st
import json
import os
import time

# ─── Backend Modules ─────────────────────────────────────────
from modules.scraper import fetch_and_scrape
from modules.deduplicator import deduplicate
from modules.stance_filter import label_and_balance_articles
from modules.database import ingest_to_chroma, query_chroma
from modules.nlp_analyzer import analyze_articles, validate_against_gemini
from modules.visualizer import (
    generate_sentiment_chart,
    generate_bias_spectrum,
    generate_entity_chart,
    generate_wordcloud,
    generate_speedometer,
    generate_radar_chart
)
from modules.agent_analyst import agent_analyst
from modules.agent_critic import agent_critic
from modules.agent_arbitrator import agent_arbitrator
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()
from modules.intent_decoder import decode_intent
from modules.scraper import fetch_multiple_queries

# ─── Page Config ───────────────────────────────────────────
st.set_page_config(
    page_title="ORBITA | Advanced Analysis",
    page_icon="🔭",
    layout="wide"
)

# ─── Custom Premium CSS ────────────────────────────────────
st.markdown("""
    <style>
    .main { background-color: #0f1117; }
    .block-container { padding-top: 2rem; }
    .orb-metric-card {
        background-color: #1e1e2e; border-radius: 12px; padding: 20px; text-align: center; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.3); margin-bottom: 20px;
    }
    .agent-box {
        background-color: #1e1e2e; border-radius: 12px; padding: 20px; 
        margin-bottom: 20px; border-left: 4px solid;
    }
    .agent-a { border-color: #2ecc71; }
    .agent-b { border-color: #e74c3c; }
    .agent-c { border-color: #3498db; }
    .log-ok { color: #2ecc71; font-family: monospace; }
    .log-run { color: #f1c40f; font-family: monospace; }
    .validation-badge {
        padding: 15px; border-radius: 8px; text-align: center; 
        font-weight: bold; font-size: 18px; margin: 20px 0;
    }
    </style>
""", unsafe_allow_html=True)

# ─── Header ────────────────────────────────────────────────
st.markdown("""
    <h1 style='text-align:center; color:#a29bfe;'>
        🔭 ORBITA Engine
    </h1>
    <p style='text-align:center; color:#dfe6e9; font-size:16px;'>
        Objective Reasoning And Bias Interpretation Tool for Analysis
    </p>
    <hr style='border: 1px solid #2d2d2d;'>
""", unsafe_allow_html=True)

# ─── Sidebar Controls ──────────────────────────────────────
st.sidebar.image("https://img.icons8.com/fluency/96/satellite.png", width=80)
st.sidebar.title("ORBITA Controls")
st.sidebar.markdown("---")

mode = st.sidebar.radio(
    "Select Mode",
    ["🔍 Scrape New Topic", "📂 Use Existing Collection"]
)

st.sidebar.markdown("---")
topic = st.sidebar.text_input("Enter Topic to Analyze", placeholder="e.g. Artificial Intelligence vs Jobs")

# ─── Mode 1: Scrape New Topic (With Hacker Logs) ───────────
if mode == "🔍 Scrape New Topic":
    collection_name = st.sidebar.text_input("Collection Name (for saving)", placeholder="e.g. ai_vs_jobs")
    scrape_btn = st.sidebar.button("🚀 Execute Analysis Pipeline")

    if scrape_btn and topic and collection_name:
        progress_bar = st.progress(0)
        log_box = st.empty()
        logs = []

        def update_log(msg, progress, done=False):
            if done and logs:
                logs[-1] = f"<span class='log-ok'>✓ {logs[-1][14:]}</span>"
            else:
                logs.append(f"<span class='log-run'>◈ {msg}</span>")
            log_box.markdown(f"<div style='background:#1e1e2e; padding:15px; border-radius:10px; border-left: 3px solid #a29bfe;'>{'<br>'.join(logs)}</div>", unsafe_allow_html=True)
            progress_bar.progress(progress)

        try:
            # Step 1: Decode Intent
            update_log("Decoding intent with spaCy NER...", 5)
            intent = decode_intent(topic)
            queries = intent["search_queries"]
            update_log(f"Intent Decoded: {len(queries)} smart queries generated", 15, done=True)

            # Step 2: Multi-Query Scrape
            update_log(f"Fetching news for: {', '.join(queries)}...", 25)
            raw_articles = fetch_multiple_queries(queries)
            update_log(f"Fetched total {len(raw_articles)} raw articles", 40, done=True)

            # Step 3: Deduplication
            update_log(f"Deduplicating {len(raw_articles)} articles...", 50)
            unique_articles = deduplicate(raw_articles)
            update_log(f"Cleaned! {len(unique_articles)} unique articles remain", 65, done=True)

            # Step 4: Stance Balancer
            update_log("Balancing Pro/Against Stances for AI Context...", 75)
            balanced_articles = label_and_balance_articles(unique_articles)
            
            filename = f"{collection_name}.json"
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(balanced_articles, f, indent=4, ensure_ascii=False)
            update_log("", 85, done=True)

            # Step 5: Database
            update_log("Embedding and Ingesting to ChromaDB...", 95)
            ingest_to_chroma(filename, collection_name)
            update_log("Pipeline Complete! Initializing Dashboard...", 100, done=True)

            # Save to session state
            st.session_state["articles"] = balanced_articles
            st.session_state["collection_name"] = collection_name
            st.session_state["topic"] = topic
            st.session_state["ready"] = True
            
            time.sleep(1.5)
            st.rerun()
            log_box.empty()
            progress_bar.empty()

        except Exception as e:
            st.error(f"❌ Pipeline Failed: {e}")

# ─── Mode 2: Use Existing Collection ──────────────────────
else:
    collection_name = st.sidebar.text_input("Existing Collection Name", placeholder="e.g. ai_vs_jobs")
    analyze_btn = st.sidebar.button("🔎 Load Dashboard")

    if analyze_btn and topic and collection_name:
        filename = f"{collection_name}.json"
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                articles = json.load(f)
            st.session_state["articles"] = articles
            st.session_state["collection_name"] = collection_name
            st.session_state["topic"] = topic
            st.session_state["ready"] = True
        else:
            st.error(f"❌ File '{filename}' not found!")

# ─── Main Dashboard ────────────────────────────────────────
if st.session_state.get("ready"):
    articles = st.session_state["articles"]
    collection_name = st.session_state["collection_name"]
    topic = st.session_state["topic"]

    # ── NLP Analysis ──
    with st.spinner("🧠 Running NLP Analytics..."):
        nlp_results = analyze_articles(articles)

    # ── Metrics Row ──
    st.markdown("### 📊 Engine Overview")
    c1, c2, c3, c4 = st.columns(4)
    overall = nlp_results["overall_sentiment"]
    border_color = "#2ecc71" if overall >= 0.05 else "#e74c3c" if overall <= -0.05 else "#3498db"
    
    def metric_card(title, val, color):
        return f"<div class='orb-metric-card' style='border-bottom: 4px solid {color};'><p style='color:#5c6b82; font-size:12px; margin:0; text-transform:uppercase; letter-spacing:1px;'>{title}</p><h2 style='color:#dfe6e9; margin:10px 0 0 0;'>{val}</h2></div>"
    
    c1.markdown(metric_card("Overall Stance", "SUPPORTIVE" if overall >= 0.05 else "CRITICAL" if overall <= -0.05 else "BALANCED", border_color), unsafe_allow_html=True)
    c2.markdown(metric_card("Avg VADER Score", f"{overall:+.2f}", border_color), unsafe_allow_html=True)
    c3.markdown(metric_card("Analyzed Articles", len(articles), "#a29bfe"), unsafe_allow_html=True)
    
    top_keyword = nlp_results["keywords"][0].upper() if nlp_results["keywords"] else "N/A"
    c4.markdown(metric_card("Top Keyword", top_keyword, "#f1c40f"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Charts Row 1: Premium Visuals ──
    col_g, col_r, col_b = st.columns([1.5, 1.5, 2])
    with col_g:
        st.markdown("<h4 style='text-align:center;'>🧭 Stance Meter</h4>", unsafe_allow_html=True)
        st.plotly_chart(generate_speedometer(overall), use_container_width=True)
    with col_r:
        st.markdown("<h4 style='text-align:center;'>🕸️ Bias Radar</h4>", unsafe_allow_html=True)
        st.plotly_chart(generate_radar_chart(nlp_results), use_container_width=True)
    with col_b:
        st.markdown("<h4 style='text-align:center;'>🎯 Bias Spectrum</h4>", unsafe_allow_html=True)
        st.plotly_chart(generate_bias_spectrum(nlp_results), use_container_width=True)

    st.markdown("---")

    # ── Charts Row 2: Standard Visuals ──
    st.markdown("### 📈 Deep Context Visuals")
    col_left, col_right = st.columns(2)
    with col_left:
        st.plotly_chart(generate_sentiment_chart(nlp_results), use_container_width=True)
    with col_right:
        st.plotly_chart(generate_entity_chart(nlp_results), use_container_width=True)

    st.markdown("### ☁️ Keywords Word Cloud")
    wordcloud_b64 = generate_wordcloud(nlp_results["keywords"])
    if "No Keywords" not in wordcloud_b64:
        st.image(f"data:image/png;base64,{wordcloud_b64}", use_container_width=True)

    st.markdown("---")

    # ── Multi-Agent Analysis ──
    st.markdown("### 🤖 Cognitive Multi-Agent Synthesis (CoT)")

    # Run Agents only if not run yet for this topic
    if "arbitrator_output" not in st.session_state or st.session_state.get("current_topic") != topic:
        with st.spinner("🔍 Agents retrieving verified context from ChromaDB..."):
            db_results = query_chroma(collection_name, topic, top_k=4)
            db_context = "\n\n".join([f"Source: [{res['source']}]\nText: {res['text']}" for res in db_results])

        with st.spinner("⏳ Agent A (Analyst) constructing factual support..."):
            st.session_state["analyst_output"] = agent_analyst(collection_name, topic, nlp_results, db_context)

        with st.spinner("⏳ Agent B (Critic) constructing factual criticism..."):
            st.session_state["critic_output"] = agent_critic(collection_name, topic, nlp_results, db_context)

        with st.spinner("⚖️ Agent C (Arbitrator) writing 8-Step CoT verdict with citations..."):
            st.session_state["arbitrator_output"] = agent_arbitrator(topic, st.session_state["analyst_output"], st.session_state["critic_output"])
            
        st.session_state["current_topic"] = topic

    analyst_output = st.session_state["analyst_output"]
    critic_output = st.session_state["critic_output"]
    arbitrator_output = st.session_state["arbitrator_output"]

    # ── Hallucination Validation Checker ──
    ai_score_str = [line for line in arbitrator_output.split('\n') if "Implicit AI Score:" in line]
    if ai_score_str:
        try:
            # Extract number safely
            gemini_score = float(ai_score_str[0].split(":")[1].strip().replace('*', '').replace(']', '').replace('[', ''))
            validation = validate_against_gemini(overall, gemini_score)
            v_level = validation["agreement_level"]
            v_color = "rgba(46, 204, 113, 0.15)" if "Strong" in v_level else "rgba(241, 196, 15, 0.15)" if "Moderate" in v_level else "rgba(231, 76, 60, 0.15)"
            text_color = "#2ecc71" if "Strong" in v_level else "#f1c40f" if "Moderate" in v_level else "#e74c3c"
            
            st.markdown(f"""
            <div class='validation-badge' style='background-color: {v_color}; color: {text_color}; border: 1px solid {text_color};'>
                🔍 AI vs Manual NLP Validation: {v_level} <br>
                <span style='font-size: 14px; color: #dfe6e9; font-weight: normal;'>
                (Mathematical VADER: {overall:+.2f} | Gemini Cognitive Score: {gemini_score:+.2f})
                </span>
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            pass # Fail silently if AI formatting is weird

    # ── Agent Outputs in Tabs ──
    tab1, tab2, tab3 = st.tabs([
        "🟢 Agent A — Analyst",
        "🔴 Agent B — Critic",
        "⚖️ Agent C — Arbitrator (Final Report)"
    ])

    with tab1:
        st.markdown(f"""
        <div class='agent-box agent-a'>
            <h4 style='color:#2ecc71;'>Agent A — Supporting Arguments</h4>
            <p style='color:#dfe6e9;'>{analyst_output.replace(chr(10), '<br>')}</p>
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        st.markdown(f"""
        <div class='agent-box agent-b'>
            <h4 style='color:#e74c3c;'>Agent B — Critical Arguments</h4>
            <p style='color:#dfe6e9;'>{critic_output.replace(chr(10), '<br>')}</p>
        </div>
        """, unsafe_allow_html=True)

    with tab3:
        st.markdown(f"""
        <div class='agent-box agent-c'>
            <h4 style='color:#3498db;'>Agent C — Chain of Thought Synthesis</h4>
            <p style='color:#dfe6e9;'>{arbitrator_output.replace(chr(10), '<br>')}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Source Transparency Table ──
    st.markdown("---")
    st.markdown(f"### ⊟ Source Transparency — {len(articles)} Articles Analyzed")
    
    for i, article in enumerate(articles, 1):
        title = (article.get("title") or "Unknown Title")[:80] + "..."
        source = article.get("source") or "Unknown"
        # We estimate word count by splitting text
        words = len((article.get("text") or "").split())
        
        # Determine Stance Pill based on VADER score
        score = analyzer.polarity_scores(article.get("text", ""))['compound'] if 'text' in article else 0
        if score >= 0.05:
            pill = "<span style='background:#2ecc7122; color:#2ecc71; padding:2px 8px; border-radius:12px; font-size:12px;'>Supportive</span>"
        elif score <= -0.05:
            pill = "<span style='background:#e74c3c22; color:#e74c3c; padding:2px 8px; border-radius:12px; font-size:12px;'>Critical</span>"
        else:
            pill = "<span style='background:#5b9cf622; color:#5b9cf6; padding:2px 8px; border-radius:12px; font-size:12px;'>Neutral</span>"

        url = article.get("url", "#")

        col_info, col_stance, col_link = st.columns([6, 2, 1])
        with col_info:
            st.markdown(
                f"<div style='color:#dfe6e9; font-weight:500; font-size:15px;'>"
                f"<span style='color:#5c6b82; font-family:monospace;'>{i:02d}</span> {title}</div>"
                f"<div style='color:#5c6b82; font-size:12px; margin-top:4px;'>"
                f"{source} • {words:,} words</div>",
                unsafe_allow_html=True
            )
        with col_stance:
            st.markdown(f"<div style='padding-top:5px;'>{pill}</div>", unsafe_allow_html=True)
        with col_link:
            st.markdown(f"<a href='{url}' target='_blank'><button style='width:100%; background:#1e1e2e; color:#a29bfe; border:1px solid #a29bfe; border-radius:6px; padding:4px;'>↗ Link</button></a>", unsafe_allow_html=True)

        st.markdown("<hr style='border-top:1px solid #2d2d2d; margin: 10px 0;'>", unsafe_allow_html=True)

    # ── Download Report ──
    st.markdown("### 💾 Export Analysis")
    report = f"""ORBITA Analysis Report
Topic: {topic}
Overall Sentiment Score (VADER): {overall:.2f}
Top Keywords: {', '.join(nlp_results['keywords'])}

=== Agent A: Supporting Side ===
{analyst_output}

=== Agent B: Critical Side ===
{critic_output}

=== Agent C: Final Balanced Report ===
{arbitrator_output}
"""
    st.download_button(
        label="📥 Download Full Report (.txt)",
        data=report,
        file_name=f"{collection_name}_report.txt",
        mime="text/plain"
    )