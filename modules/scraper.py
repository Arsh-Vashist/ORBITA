import requests
from newspaper import Article
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Safely fetch the API key
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

if not NEWS_API_KEY:
    raise ValueError("🚨 NEWS_API_KEY is missing! Please check your .env file.")

def fetch_and_scrape(user_input, limit_per_query=12):
    """
    Ek single query ke liye articles fetch aur scrape karta hai.
    """
    search_query = user_input.replace(" vs ", " AND ")
    api_url = "https://newsapi.org/v2/everything"
    params = {
        'q': search_query,
        'language': 'en',
        'sortBy': 'relevancy',
        'pageSize': 20, # Reduced payload to make it faster
        'apiKey': NEWS_API_KEY
    }

    try:
        response = requests.get(api_url, params=params)
        if response.status_code != 200:
            print(f"Error: {response.json().get('message', 'API Error')}")
            return []
        
        articles_list = response.json().get('articles', [])
        scraped_data = []

        for item in articles_list:
            # Har query se max 10-12 quality articles nikalenge
            if len(scraped_data) >= limit_per_query: 
                break
            
            # Avoid empty urls
            if not item.get('url'): continue

            try:
                article = Article(item['url'])
                article.download()
                article.parse()
                
                if len(article.text) > 300: # Only keep quality articles
                    scraped_data.append({
                        "title": item.get('title', 'No Title'),
                        "source": item.get('source', {}).get('name', 'Unknown'),
                        "text": article.text,
                        "url": item['url'] # <--- BUG FIXED: Saved URL for UI Link Button
                    })
                    print(f"✓ Scraped: {item['title'][:40]}...")
            except:
                continue
                
        return scraped_data
    except Exception as e:
        print(f"Scraper Error: {str(e)}")
        return []

def fetch_multiple_queries(queries: list) -> list:
    """
    Takes a list of search queries (from intent decoder), 
    runs the scraper for each, and combines all results into one massive list.
    """
    all_articles = []
    
    for query in queries:
        print(f"📡 Fetching data for query: '{query}'")
        # Har query se 10 articles layega (Total max ~30)
        articles = fetch_and_scrape(query, limit_per_query=10) 
        all_articles.extend(articles)
        
    return all_articles