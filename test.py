import json
from modules.scraper import fetch_and_scrape

def run_test():
    print("=== ORBITA: News Collector ===")
    topic = input("Enter news topic: ")
    filename_title = input("Enter a title for the saved file: ")
    
    # Sanitize and format filename
    filename = filename_title.strip().replace(" ", "_") + ".json"
    
    results = fetch_and_scrape(topic)
    
    if isinstance(results, list) and len(results) > 0:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4, ensure_ascii=False)
        
        print(f"\nSUCCESS! {len(results)} articles saved to {filename}")
        print("-" * 30)
        
        for i, article in enumerate(results, 1):
            print(f"{i}. {article['title']} [{article['source']}]")
            
        print("-" * 30)
        print(f"Check '{filename}' to see the full extracted text for all articles.")
    else:
        print(f"Error: {results}")

if __name__ == "__main__":
    run_test()
