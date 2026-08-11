
# chatbot/gemini_client.py

import os

from dotenv import load_dotenv
from google import genai


# ------------------------------------------------------------
# Load environment variables
# ------------------------------------------------------------

load_dotenv()


# ------------------------------------------------------------
# Gemini Configuration
# ------------------------------------------------------------

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY was not found. "
        "Please add it to your .env file."
    )


# ------------------------------------------------------------
# Gemini Client
# ------------------------------------------------------------

client = genai.Client(api_key=GEMINI_API_KEY)


# ------------------------------------------------------------
# Generate Response
# ------------------------------------------------------------

def generate_response(prompt):
    """
    Send a prompt to Gemini and return the generated response.

    Args:
        prompt (str): Prompt/question sent to Gemini.

    Returns:
        str: Gemini's response.
    """

    if not prompt or not prompt.strip():
        return "Please provide a question."

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        if response and response.text:
            return response.text.strip()

        return "Gemini returned an empty response."

    except Exception as e:
        print(f"Gemini API Error: {e}")

        return (
            "Sorry, I couldn't process your request right now. "
            "Please try again."
        )
