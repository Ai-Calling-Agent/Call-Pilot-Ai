import os
from groq import Groq
from dotenv import load_dotenv

import os
from groq import Groq
import os


load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

async def get_real_estate_response(user_input: str):
    prompt = f"""
You are a real estate sales representative.
You're making an outbound call to a prospective client.
Always be polite, helpful, and persuasive.

Client: {user_input}
You:
"""
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama3-8b-8192",
            temperature=0.7,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"