from modules.database import ingest_to_chroma
import json

def run_test():
    print("=== ORBITA: ChromaDB Ingestion ===")
    filename = input("Enter JSON filename to ingest (e.g. AI_News_March.json): ").strip()
    collection_name = filename.replace(".json", "")

    # DEBUG: check if file loads correctly
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(f"DEBUG: Found {len(data)} articles in {filename}")

    ingest_to_chroma(filename, collection_name)
    print(f"\n📦 Data is now stored in ChromaDB under collection: '{collection_name}'")

if __name__ == "__main__":
    run_test()