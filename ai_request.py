from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ai_request(file1, file2):
    """Compare two strings."""

    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": f"Hello, are the two strings '{file1}' and '{file2}' the same?"}])

    return response.choices[0].message.content
