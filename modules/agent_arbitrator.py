from modules.llm import ask_llm

def agent_arbitrator(topic: str, analyst_output: str, critic_output: str) -> str:
    prompt = f"""
You are ORBITA - an elite, unbiased news analysis AI. 
Your task is to synthesize conflicting arguments into a perfectly balanced report using advanced Chain of Thought reasoning.

Topic: {topic}

=== Pre-analyzed Supporting Side (Agent A) ===
{analyst_output}

=== Pre-analyzed Critical Side (Agent B) ===
{critic_output}

Now, execute the following 8 steps ONE BY ONE. Show your reasoning for each step clearly:

Step 1 - CORE UNDERSTANDING: 
What is the fundamental issue or conflict here? Summarize the crux of the debate in 2-3 lines.

Step 2 - DECONSTRUCT SUPPORT: 
Analyze Agent A's side. Which of their points are backed by hard facts or data? Which points rely on emotion, speculation, or rhetoric? List them.

Step 3 - DECONSTRUCT CRITICISM: 
Analyze Agent B's side. Which of their points are backed by hard facts or data? Which points rely on emotion, speculation, or rhetoric? List them.

Step 4 - CORROBORATION (COMMON GROUND): 
Identify specific facts or events where BOTH sides completely agree. 

Step 5 - CONTRADICTION ANALYSIS: 
Identify the exact points where the two sides directly contradict each other. Why is there a mismatch? (e.g., different data sources, different interpretations).

Step 6 - BIAS & MANIPULATION DETECTION: 
Examine the language and sources from both sides. Is one side using more sensationalism or biased framing? Explain briefly.

Step 7 - SYNTHESIS REPORT (CRITICAL STEP): 
Write a balanced, unbiased, and factual 150-word final summary. Do not take any sides. 
CONSTRAINT: You MUST include "Real Citations". Every time you state a fact or argument in this summary, you MUST append the exact source name in brackets right next to it based on the inputs provided. 
Example: "The bill was passed with a 60% majority [Source: Reuters], though critics argue it harms local businesses [Source: Fox News]."

Step 8 - FINAL SCORING: 
End your entire response with exactly these two lines based on your deep analysis:
"Bias Level: [Low / Medium / High]"
"Implicit AI Score: [Provide a single float number between -1.0 (Highly Negative/Critical) to 1.0 (Highly Positive/Supportive) representing the true overall stance of the analyzed data]"
"""
    return ask_llm(prompt)