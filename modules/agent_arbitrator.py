from modules.llm import ask_llm

def agent_arbitrator(topic: str, analyst_output: str, critic_output: str) -> str:

    prompt = f"""
You are Agent C - The Arbitrator.

Topic: {topic}

Side A Analysis:
{analyst_output}

Side B Analysis:
{critic_output}

Your Job:
- Cross-check both sides using facts
- Identify which claims are factually strong and which are weak
- Write a final UNBIASED, BALANCED report
- Avoid loaded language or taking any side
- Format: 
  * Key Facts
  * Side A Strengths & Weaknesses
  * Side B Strengths & Weaknesses
  * Final Verdict

Final Balanced Report:
"""
    return ask_llm(prompt)