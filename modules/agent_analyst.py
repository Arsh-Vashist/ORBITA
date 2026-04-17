from modules.llm import ask_llm

def agent_analyst(collection_name: str, topic: str, nlp_results: dict = None, db_context: str = "") -> str:
    if not nlp_results:
        return "No NLP results available."

    pro_articles = [a for a in nlp_results["articles"] if "Pro" in a["bias"] or a["sentiment_score"] > 0.05]
    if not pro_articles:
         pro_articles = sorted(nlp_results["articles"], key=lambda x: x["sentiment_score"], reverse=True)[:5]

    nlp_stats_text = "\n".join([f"- [{a['source']}] {a['title']} (Score: {a['sentiment_score']:.2f}, Entities: {', '.join(a['entities']['PERSON'][:2])})" for a in pro_articles[:5]])

    side_a = topic.split(" vs ")[0].strip() if " vs " in topic.lower() else topic

    prompt = f"""
    You are ORBITA's Analyst Agent. Your job is to construct the strongest possible SUPPORTING arguments for: {side_a}

    Here is the manual NLP statistical data (Vader Sentiment & NER) for the most positive articles:
    {nlp_stats_text}
    Keywords found: {', '.join(nlp_results['keywords'][:5])}

    Here is the actual context retrieved from the database:
    {db_context}

    Using BOTH the statistical NLP data and the text context, write a 150-word synthesis supporting {side_a}.
    Explicitly mention the sentiment trends and key entities found by the NLP engine.
    """
    return ask_llm(prompt)