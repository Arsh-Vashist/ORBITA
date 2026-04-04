from modules.database import query_chroma
from modules.llm import ask_llm

def agent_critic(collection_name: str, topic: str) -> str:
    
    # Fetch top 5 relevant chunks from ChromaDB
    results = query_chroma(collection_name, topic, top_k=5)
    
    # Combine all chunks into one string with source names
    context = "\n\n".join([f"[{r['source']}]: {r['text']}" for r in results])

    # Detect if topic has two sides (vs) or is a general topic
    if " vs " in topic.lower():
        sides = topic.lower().split(" vs ")
        instruction = f"Extract arguments and claims made by or in favor of: {sides[1].strip().upper()}"
    else:
        instruction = "Extract all NEGATIVE, CRITICAL, and OPPOSING arguments about the topic"

    prompt = f"""
You are Agent B - The Critic.

Topic: {topic}

Context from News Articles:
{context}

Your Job: {instruction}

Instructions:
- Be specific and use facts from the articles
- Format as numbered points
- Do not include the opposing side

Analysis:
"""
    return ask_llm(prompt)