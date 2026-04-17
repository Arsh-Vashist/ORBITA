import spacy

# Ensure spacy model is loaded
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import os
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

def decode_intent(user_input: str) -> dict:
    """
    Analyzes user input using spaCy NER and constructs 
    multiple search queries for broader NewsAPI coverage.
    """
    print(f"🧠 Decoding intent for: '{user_input}'")
    doc = nlp(user_input)
    
    entities = [ent.text for ent in doc.ents]
    keywords = [token.text for token in doc if token.is_alpha and not token.is_stop]
    
    # Base query is the original input
    queries = [user_input]
    
    # Generate variations
    if entities:
        # Query based on named entities + "news"
        queries.append(f"{' '.join(entities)} news")
        # Query based on entities + "controversy" or "debate" for unbiased fetching
        queries.append(f"{' '.join(entities)} debate")
    elif len(keywords) > 1:
        queries.append(f"{' '.join(keywords)} overview")
    
    # Remove duplicates and limit to 3 queries
    queries = list(set(queries))[:3]
    
    print(f"🎯 Generated Search Queries: {queries}")
    
    return {
        "topic": user_input,
        "search_queries": queries,
        "entities_found": entities
    }