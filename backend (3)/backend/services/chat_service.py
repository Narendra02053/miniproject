import os
from groq import Groq
from dotenv import load_dotenv
from functools import lru_cache

load_dotenv()

@lru_cache(maxsize=1)
def get_groq_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError(
            "❌ GROQ_API_KEY not found in .env file.\n"
            "Create a free key at https://console.groq.com"
        )
    return Groq(api_key=api_key)


def chat_with_ai(user_message: str) -> str:
    if not user_message.strip():
        return "Please type a message."

    client = get_groq_client()

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a friendly helpful study assistant. "
                        "Explain concepts clearly and simply."
                    ),
                },
                {"role": "user", "content": user_message},
            ],
            max_tokens=300,
            temperature=0.7,
        )

        # ✅ FIX: Extract content correctly
        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"[GROQ CHAT ERROR] {e}")
        return "Sorry, I couldn’t process your message. Try again."
