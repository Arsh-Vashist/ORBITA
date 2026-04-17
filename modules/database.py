import json
import chromadb
from sentence_transformers import SentenceTransformer

CHROMA_DB_PATH = "./chroma_db"
model = SentenceTransformer("all-MiniLM-L6-v2")

def load_json(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

def chunk_text(text, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
        i += chunk_size - overlap
    return chunks

def ingest_to_chroma(filename, collection_name):
    articles = load_json(filename)

    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    collection = client.get_or_create_collection(name=collection_name)

    print("Ingesting... please wait\n")

    doc_id = 0
    for i, article in enumerate(articles):
        try:
            chunks = chunk_text(article["text"])
            embeddings = model.encode(chunks).tolist()

            for chunk, embedding in zip(chunks, embeddings):
                collection.add(
                    documents=[chunk],
                    embeddings=[embedding],
                    metadatas=[{
                        "title": article["title"],
                        "source": article["source"],
                        "topic": collection_name
                    }],
                    ids=[f"{collection_name}_{doc_id}"]
                )
                doc_id += 1

            print(f"✓ Article {i+1}/{len(articles)}: {article['title'][:50]}...")
        except Exception as e:
            print(f"❌ Failed on article {i+1}: {e}")
            continue

    print(f"\nIngested {len(articles)} articles into collection: '{collection_name}'")
    print(f"   Total chunks stored: {doc_id}")
    return doc_id

def query_chroma(collection_name, query, top_k=5):
    """
    Searches ChromaDB for the most relevant chunks to the query.
    Returns top_k results with their text and metadata.
    """
    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    
    try:
        collection = client.get_collection(name=collection_name)
    except Exception:
        print(f"Collection '{collection_name}' not found in ChromaDB.")
        return []

    # Embed the query using the same model
    query_embedding = model.encode([query]).tolist()

    # Search ChromaDB for most similar chunks
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )

    # Format results into a clean list
    formatted = []
    for i in range(len(results["documents"][0])):
        formatted.append({
            "text": results["documents"][0][i],
            "title": results["metadatas"][0][i]["title"],
            "source": results["metadatas"][0][i]["source"],
            "score": round(1 - results["distances"][0][i], 3)  # convert distance to similarity
        })

    return formatted
