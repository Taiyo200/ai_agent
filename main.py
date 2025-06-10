import os
from dotenv import load_dotenv
from google import genai
import sys

load_dotenv("env/gemini_api.env")
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

if sys.argv is not None and len(sys.argv) > 1:
    prompt = sys.argv[1]
else:
    raise ValueError("Please provide a prompt as a command line argument.")

answer = client.models.generate_content(model="gemini-2.0-flash-001", contents=prompt)

token_count = answer.usage_metadata.prompt_token_count 
candidates_count = answer.usage_metadata.candidates_token_count

if "--verbose" in sys.argv or "-v" in sys.argv:
    print(f"User prompt:\n{prompt}\n\nAnswer:\n{answer.text}\n\nPrompt tokens: {token_count}\n\nResponse tokens: {candidates_count}")

else:
    print(answer.text)
