from modules.agent_analyst import agent_analyst
from modules.agent_critic import agent_critic
from modules.agent_arbitrator import agent_arbitrator

def run_orbita():
    print("=== ORBITA: Multi-Agent Analysis ===\n")
    
    # User input
    collection_name = input("Enter collection name: ").strip()
    topic = input("Enter topic to analyze: ").strip()

    print("\nAgent A (Analyst) working...\n")
    analyst_output = agent_analyst(collection_name, topic)
    print("=== Agent A: Supporting Side ===")
    print(analyst_output)

    print("\nAgent B (Critic) working...\n")
    critic_output = agent_critic(collection_name, topic)
    print("=== Agent B: Critical Side ===")
    print(critic_output)

    print("\nAgent C (Arbitrator) working...\n")
    arbitrator_output = agent_arbitrator(topic, analyst_output, critic_output)
    print("=== Agent C: Final Balanced Report ===")
    print(arbitrator_output)

    # Save report to a file
    filename = f"{collection_name}_report.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"Topic: {topic}\n\n")
        f.write("=== Agent A: Supporting Side ===\n")
        f.write(analyst_output + "\n\n")
        f.write("=== Agent B: Critical Side ===\n")
        f.write(critic_output + "\n\n")
        f.write("=== Agent C: Final Balanced Report ===\n")
        f.write(arbitrator_output)
    
    print(f"\nReport saved to '{filename}'")

if __name__ == "__main__":
    run_orbita()