import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = "gemini-2.5-flash-lite"

def ask_llm(prompt: str, retries: int = 3) -> str:
    """
    Calls the LLM and automatically retries if the server is overloaded (503) 
    or quota is exhausted (429).
    """
    for attempt in range(retries):
        try:
            # 5 second buffer before call
            time.sleep(5)
            response = client.models.generate_content(
                model=MODEL,
                contents=prompt
            )
            return response.text
            
        except Exception as e:
            error_str = str(e)
            # Agar server busy (503) hai ya API limit (429) hit hui hai
            if "503" in error_str or "429" in error_str:
                wait_time = 15 * (attempt + 1) # Pehli baar 15s wait, dusri baar 30s
                print(f"⚠️ API Busy (Error {error_str}). Retrying in {wait_time} seconds... (Attempt {attempt + 1}/{retries})")
                time.sleep(wait_time)
            else:
                # Koi aur error ho toh turant return kar do
                return f"❌ LLM Error: {e}"
                
    return "❌ LLM Error: Gemini servers are experiencing extremely high demand right now. Please try again after 5-10 minutes."