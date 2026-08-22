import os
import json

from groq import Groq
from pathlib import Path
from dotenv import load_dotenv

from backend.prompts import SYSTEM_PROMPT


load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found in .env")


client = Groq(api_key=api_key)


BASE_DIR = Path(__file__).resolve().parent.parent
PROFILE_PATH = BASE_DIR / "data" / "public_profile.json"


with open(PROFILE_PATH, "r", encoding="utf-8") as file:
    profile = json.load(file)


PROFILE_TEXT = json.dumps(profile, indent=2)


def generate_response(user_message: str):

    system_message = f"""
{SYSTEM_PROMPT}

Here is Harsh Ingle's profile:

{PROFILE_TEXT}
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": system_message
            },
            {
                "role": "user",
                "content": user_message
            }
        ],
        temperature=0.3
    )

    return response.choices[0].message.content