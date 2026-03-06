import os
import requests
from newspaper import Article
from dotenv import load_dotenv

load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def fetch_and_scrape(user_input):
    search_query = user_input.replace(" vs ", " AND ")
    api_url = "https://newsapi.org/v2/everything"
    params = {
        'q': search_query,
        'language': 'en',
        'sortBy': 'relevancy',
        'pageSize': 35, # Fetch extra to ensure we hit 20-30 after failures
        'apiKey': NEWS_API_KEY
    }

    try:
        response = requests.get(api_url, params=params)
        if response.status_code != 200:
            return f"Error: {response.json().get('message', 'API Error')}"
        
        articles_list = response.json().get('articles', [])
        scraped_data = []

        for item in articles_list:
            if len(scraped_data) >= 30: break
            try:
                article = Article(item['url'])
                article.download()
                article.parse()
                if len(article.text) > 300: # Only keep quality articles
                    scraped_data.append({
                        "title": item['title'],
                        "source": item['source']['name'],
                        "text": article.text
                    })
                    print(f"✓ Scraped: {item['title'][:40]}...")
            except:
                continue
        return scraped_data
    except Exception as e:
        return str(e)