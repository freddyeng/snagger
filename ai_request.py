from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

  # recommended to store in environment variable

# 4. Make a simple request
response = client.chat.completions.create(model="gpt-3.5-turbo",
messages=[{"role": "user", "content": "Hello, what is 2+2?"}])

# 5. Print the response
print(response.choices[0].message.content)
