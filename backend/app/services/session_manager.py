import os
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = AsyncOpenAI(api_key=api_key) if api_key else None

class SessionManager:
    def __init__(self):
        self.transcripts = {} # session_id -> list of strings

    def add_to_transcript(self, session_id: str, text: str):
        if session_id not in self.transcripts:
            self.transcripts[session_id] = []
        self.transcripts[session_id].append(text)

    def get_full_transcript(self, session_id: str) -> str:
        return " ".join(self.transcripts.get(session_id, []))

    async def generate_summary(self, session_id: str):
        full_text = self.get_full_transcript(session_id)
        if not full_text:
            return "No transcript available."

        if os.getenv("OPENAI_API_KEY"):
            try:
                response = await client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a sales manager. Summarize the following sales call transcript and provide 3 actionable insights for the sales representative."},
                        {"role": "user", "content": full_text}
                    ]
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                return f"Error generating summary: {e}"
        
        # Fallback
        return f"Summary (Mock): The call covered various topics including {full_text[:50]}... Performance seems stable."

# Global singleton for simplicity in this prototype
session_manager = SessionManager()
