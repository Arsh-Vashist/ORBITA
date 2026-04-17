from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def label_and_balance_articles(articles):
    """
    1. VADER use karke har article ka stance (Pro/Against/Neutral) nikalta hai.
    2. Data ko 50-50 balance karta hai taaki AI unbiased rahe.
    """
    print(f"⚖️ Balancing Stance for {len(articles)} articles...")
    
    pro_articles = []
    against_articles = []
    neutral_articles = []

    # Step 1: Label all articles
    for article in articles:
        text = article.get("text", "")
        if not text: continue
            
        score = analyzer.polarity_scores(text)['compound']
        
        if score >= 0.05:
            pro_articles.append(article)
        elif score <= -0.05:
            against_articles.append(article)
        else:
            neutral_articles.append(article)

    print(f"📊 Before Balance -> Pro: {len(pro_articles)} | Against: {len(against_articles)} | Neutral: {len(neutral_articles)}")

    # Step 2: Balance the dataset (Match the minority class)
    # Agar 20 Pro hain aur 10 Against hain, toh hum dono ko 10-10 kar denge
    min_count = min(len(pro_articles), len(against_articles))
    
    # Agar koi ek side bilkul hi 0 hai (highly biased topic), toh hum maximum 5 ka difference allow karenge
    if min_count == 0:
        balanced_pro = pro_articles[:5]
        balanced_against = against_articles[:5]
    else:
        # Sort karke sabse strong articles lenge
        pro_articles.sort(key=lambda x: analyzer.polarity_scores(x["text"])['compound'], reverse=True)
        against_articles.sort(key=lambda x: analyzer.polarity_scores(x["text"])['compound'])
        
        balanced_pro = pro_articles[:min_count]
        balanced_against = against_articles[:min_count]

    # Neutral articles bhi add kar dete hain context ke liye (max 5)
    balanced_dataset = balanced_pro + balanced_against + neutral_articles[:5]
    
    print(f"✅ After Balance  -> Pro: {len(balanced_pro)} | Against: {len(balanced_against)} | Neutral: {len(neutral_articles[:5])}")
    
    return balanced_dataset