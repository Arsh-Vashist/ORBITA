import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

print("Fetching available models...\n")
for model in client.models.list():
    # Hum sirf fast/flash models filter kar rahe hain
    if "flash" in model.name.lower() or "pro" in model.name.lower():
        print(f"✅ Exact Name to use: {model.name}")