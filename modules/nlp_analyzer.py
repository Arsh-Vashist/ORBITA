import spacy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter

nlp = spacy.load("en_core_web_sm")
analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    scores = analyzer.polarity_scores(text)
    compound = scores['compound']
    if compound >= 0.05:
        label = "Positive"
    elif compound <= -0.05:
        label = "Negative"
    else:
        label = "Neutral"
    return {"score": compound, "label": label}

def extract_entities(text):
    doc = nlp(text)
    entities = {"PERSON": [], "ORG": [], "GPE": []}
    for ent in doc.ents:
        if ent.label_ in entities:
            entities[ent.label_].append(ent.text)
    entities["PERSON"] = list(set(entities["PERSON"]))
    entities["ORG"] = list(set(entities["ORG"]))
    entities["GPE"] = list(set(entities["GPE"]))
    return entities

def extract_keywords(texts, top_n=10):
    vectorizer = TfidfVectorizer(stop_words='english', max_features=100)
    vectorizer.fit_transform(texts)
    scores = zip(vectorizer.get_feature_names_out(),
                 vectorizer.idf_)
    sorted_scores = sorted(scores, key=lambda x: x[1])
    return [word for word, score in sorted_scores[:top_n]]

def calculate_bias_score(sentiment_score):
    if sentiment_score >= 0.5:
        return "Strongly Pro"
    elif sentiment_score >= 0.05:
        return "Mildly Pro"
    elif sentiment_score <= -0.5:
        return "Strongly Against"
    elif sentiment_score <= -0.05:
        return "Mildly Against"
    else:
        return "Neutral"

def analyze_articles(articles):
    results = []
    all_texts = [a["text"] for a in articles]
    keywords = extract_keywords(all_texts)

    for article in articles:
        sentiment = analyze_sentiment(article["text"])
        entities = extract_entities(article["text"])
        bias = calculate_bias_score(sentiment["score"])

        results.append({
            "title": article["title"],
            "source": article["source"],
            "sentiment_score": sentiment["score"],
            "sentiment_label": sentiment["label"],
            "bias": bias,
            "entities": entities
        })

    return {
        "articles": results,
        "keywords": keywords,
        "overall_sentiment": sum(r["sentiment_score"] for r in results) / len(results)
    }

def validate_against_gemini(manual_score, gemini_score):
    """
    Compares the mathematical VADER sentiment score with Gemini's interpreted bias score.
    Returns the level of agreement to prove the AI is not hallucinating.
    """
    diff = abs(manual_score - gemini_score)
    
    # Check if both scores point in the same direction (e.g., both positive or both negative)
    same_direction = (manual_score >= 0 and gemini_score >= 0) or (manual_score < 0 and gemini_score < 0)
    
    if diff <= 0.2 and same_direction:
        agreement = "🟢 Strong Agreement (Highly Reliable)"
    elif diff <= 0.4 and same_direction:
        agreement = "🟡 Moderate Agreement (Reliable)"
    elif not same_direction and diff > 0.5:
        agreement = "🔴 Contradiction (AI Hallucination Risk)"
    else:
        agreement = "⚪ Weak Agreement"
        
    return {
        "agreement_level": agreement,
        "absolute_diff": diff,
        "direction_agrees": same_direction
    }