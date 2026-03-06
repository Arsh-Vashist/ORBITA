from modules.database import query_chroma

def run_search():
    print("=== ORBITA: Search Test ===")
    collection_name = input("Enter collection name to search (e.g. MODI_and_Carney): ").strip()
    
    while True:
        print("\n(type 'exit' to quit)")
        query = input("Enter your query: ").strip()
        
        if query.lower() == "exit":
            print("Goodbye!")
            break

        results = query_chroma(collection_name, query, top_k=3)

        if not results:
            print("No results found.")
            continue

        print(f"\nTop {len(results)} results for: '{query}'")
        print("-" * 50)

        for i, r in enumerate(results, 1):
            print(f"\n{i}. [{r['source']}] {r['title'][:60]}...")
            print(f"   Relevance Score: {r['score']}")
            print(f"   Text: {r['text'][:200]}...")

        print("-" * 50)

if __name__ == "__main__":
    run_search()
