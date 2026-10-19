import os
import json

from google import genai
from google.genai import types


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_ai_analysis(title: str, content: str):
    print("TITLE RECEIVED:", title)
    print("CONTENT RECEIVED:", content)

    prompt = f"""
Analyze the following content.

Title:
{title}

Content:
{content}

Generate:
1. A short summary of the content.
2. 3 to 5 relevant tags.

Return ONLY valid JSON in exactly this format:

{{
    "summary": "short summary here",
    "tags": ["tag1", "tag2", "tag3"]
}}
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(
            automatic_function_calling=types.AutomaticFunctionCallingConfig(
                disable=True
            ),
            response_mime_type="application/json"
        )
    )

    print("RESPONSE TEXT:", response.text)

    return json.loads(response.text)

def generate_api_schema(prompt: str):
    print("API BUILDER PROMPT:", prompt)

    schema_prompt = f"""
You are an API schema generator.

The developer will describe an API they want to create.

Developer request:
{prompt}

Convert the request into a structured API schema.

Rules:

1. Identify a suitable resource_name.
2. Provide a short description.
3. Identify all relevant fields.
4. Every field must have:
   - name
   - type
   - required
5. Allowed field types are ONLY:
   - string
   - integer
   - float
   - boolean
6. Do not add fields that are unrelated to the developer's request.
7. Return ONLY valid JSON.
8. Do not include markdown.
9. Do not include explanations outside the JSON.

Return JSON in exactly this structure:

{{
    "resource_name": "products",
    "description": "E-commerce product API",
    "fields": [
        {{
            "name": "items",
            "type": "string",
            "required": true
        }},
        {{
            "name": "price",
            "type": "float",
            "required": true
        }},
        {{
            "name": "ratings",
            "type": "float",
            "required": false
        }},
        {{
            "name": "stock_status",
            "type": "boolean",
            "required": true
        }}
    ]
}}
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=schema_prompt,
        config=types.GenerateContentConfig(
            automatic_function_calling=types.AutomaticFunctionCallingConfig(
                disable=True
            ),
            response_mime_type="application/json"
        )
    )

    print("API SCHEMA RESPONSE:", response.text)

    return json.loads(response.text)