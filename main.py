import json
from modules.agent_analyst import agent_analyst
from modules.agent_critic import agent_critic
from modules.agent_arbitrator import agent_arbitrator
from modules.nlp_analyzer import analyze_articles
from modules.visualizer import save_charts
from modules.database import query_chroma

def run_orbita():
    print("=== ORBITA: Multi-Agent Analysis ===\n")

    collection_name = input("Enter collection name: ").strip()
    topic = input("Enter topic to analyze: ").strip()

    # Load articles from JSON
    filename = collection_name + ".json"
    with open(filename, "r", encoding="utf-8") as f:
        articles = json.load(f)

    # Phase 1: NLP Analysis
    print("\nRunning NLP Analysis...\n")
    nlp_results = analyze_articles(articles)

    print(f"Overall Sentiment: {nlp_results['overall_sentiment']:.2f}")
    print(f"Top Keywords: {', '.join(nlp_results['keywords'])}")
    print(f"Articles Analyzed: {len(nlp_results['articles'])}")

    # Phase 2: Generate Charts
    print("\nGenerating Charts...\n")
    save_charts(nlp_results)

    # Phase 3: Agents
    print("\nRetrieving context from ChromaDB...\n")
    db_results = query_chroma(collection_name, topic, top_k=3)
    db_context = "\n\n".join([f"Text: {res['text']}" for res in db_results])

    print("\nAgent A (Analyst) working...\n")
    analyst_output = agent_analyst(collection_name, topic, nlp_results, db_context)
    print("=== Agent A: Supporting Side ===")
    print(analyst_output)

    print("\nAgent B (Critic) working...\n")
    critic_output = agent_critic(collection_name, topic, nlp_results, db_context)
    print("=== Agent B: Critical Side ===")
    print(critic_output)

    print("\nAgent C (Arbitrator) working...\n")
    arbitrator_output = agent_arbitrator(topic, analyst_output, critic_output)
    print("=== Agent C: Final Balanced Report ===")
    print(arbitrator_output)

    # Save report
    report_filename = f"{collection_name}_report.txt"
    with open(report_filename, "w", encoding="utf-8") as f:
        f.write(f"Topic: {topic}\n\n")
        f.write(f"Overall Sentiment Score: {nlp_results['overall_sentiment']:.2f}\n")
        f.write(f"Top Keywords: {', '.join(nlp_results['keywords'])}\n\n")
        f.write("=== Agent A: Supporting Side ===\n")
        f.write(analyst_output + "\n\n")
        f.write("=== Agent B: Critical Side ===\n")
        f.write(critic_output + "\n\n")
        f.write("=== Agent C: Final Balanced Report ===\n")
        f.write(arbitrator_output)

    print(f"\nReport saved to '{report_filename}'")

if __name__ == "__main__":
    run_orbita()