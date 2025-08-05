import os
from groq import Groq

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
            model="mixtral-8x7b-32768",
            temperature=0.7,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"