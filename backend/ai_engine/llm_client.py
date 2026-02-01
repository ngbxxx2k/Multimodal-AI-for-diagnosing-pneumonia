from groq import Groq
import os

API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = "llama-3.3-70b-versatile"

class LLMClient:
    def __init__(self):
        if not API_KEY:
            self.mock = True
            self.client = None
            print("WARNING: GROQ_API_KEY not found. Using Mock mode.")
        else:
            self.mock = False
            self.client = Groq(api_key=API_KEY)

    def generate_text(self, system_prompt: str, user_input: str) -> str:
        if self.mock:
            return f"""[MOCK OUTPUT]
System Prompt: {system_prompt[:80]}
User Input: {user_input[:80]}
"""

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": user_input,
                    }
                ],
                model=MODEL_NAME,
            )
            return chat_completion.choices[0].message.content

        except Exception as e:
            return f"LLM Generation Error: {str(e)}"
