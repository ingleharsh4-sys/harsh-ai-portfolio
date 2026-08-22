import os
import json

from dotenv import load_dotenv
from groq import Groq

from prompts import SYSTEM_PROMPT


# Load environment variables
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found in .env file")


# Create Groq client
client = Groq(api_key=api_key)


# Load Harsh's profile
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PROFILE_PATH = BASE_DIR / "data" / "profile.json"

with open(PROFILE_PATH, "r", encoding="utf-8") as file:
    profile = json.load(file)


# Convert profile into text for the model
profile_text = json.dumps(profile, indent=2)


# Combine system instructions and profile
system_message = SYSTEM_PROMPT + """

Here is Harsh's current professional profile:

""" + profile_text


# Ask the model
response = client.chat.completions.create(
    model="openai/gpt-oss-120b",

    messages=[
        {
            "role": "system",
            "content": system_message
        },
        {
            "role": "user",
            "content": "Harsh worked at Google for two years, right?"
        }
    ]
)


# Print response
print("\nAI Portfolio Assistant:\n")
print(response.choices[0].message.content)