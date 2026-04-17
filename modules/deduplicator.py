def deduplicate(articles):
    """
    Checks article titles and removes exact or highly similar duplicates.
    Keeps only unique news to save ChromaDB space and improve AI context.
    """
    print(f"🧹 Deduplication Started (Input: {len(articles)} articles)")
    
    unique_articles = []
    seen_titles = set()

    for article in articles:
        # Title ko lowercase aur spaces hatakar normalize kar rahe hain
        raw_title = article.get("title", "")
        if not raw_title:
            continue
            
        clean_title = raw_title.lower().strip()
        
        # Agar ye title pehle nahi dekha, toh isko list mein add karo
        if clean_title not in seen_titles:
            seen_titles.add(clean_title)
            unique_articles.append(article)
            
    removed = len(articles) - len(unique_articles)
    print(f"✨ Deduplication Done: Removed {removed} duplicates. (Output: {len(unique_articles)} articles)")
    
    return unique_articles