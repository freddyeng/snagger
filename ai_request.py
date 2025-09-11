from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# def ai_request(file1, file2):
def ai_request(file):
    """Compare two strings."""

    # response = client.chat.completions.create(model="gpt-3.5-turbo",
    # messages=[{"role": "user", "content": f"Hello, are the two strings '{file1}' and '{file2}' the same?"}])

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a document parser. Extract structured order data from text. "
                    "Return ONLY valid JSON, no explanations."
                    "If any field is missing, set it to null instead of guessing."
                    "For each item, if there is extra information, please add as an array inside 'notes'."
                    "Extract all totals as key-value pairs."
                    "The key should be exactly the text label found in the document (before the number)."
                    "If the value is on the next line, still capture it."
                    "Remove currency symbols and convert to numbers."
                    "Include all totals found; do not guess missing ones."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Extract all items, codes, notes, quantities, and prices from this document:\n\n"
                    f"{file}\n\n"
                    "Schema:\n"
                    "{\n"
                    "  'order_id': string,\n"
                    "  'items': [\n"
                    "    {\n"
                    "      'item_name': string,\n"
                    "      'item_code': string or null,\n"
                    "      'quantity': number or null,\n"
                    "      'unit_price': number or null,\n"
                    "      'notes': array of strings or null,\n"
                    "      'total_price': number or null\n"
                    "    }\n"
                    "  ],\n"
                    "  'grand_totals': {}\n"
                    "}"
                )
            }
        ],
        max_tokens=800,
        response_format={ "type": "json_object" }  # forces JSON in new API
    )

    return response.choices[0].message.content
