from modules.agent_analyst import agent_analyst

print("----- Agent A: The Analyst -----\n")

collection_name = input("Enter collection name: ").strip()
topic = input("Enter topic to analyze: ").strip()

print("\nAnalyzing supporting arguments...\n")

result = agent_analyst(collection_name, topic)
print(result)