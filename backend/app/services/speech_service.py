import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

async def process_audio_chunk(audio_data: str) -> str:
    """
    Processes audio chunk. 
    1. If `audio_data` is text (simulation), returns it.
    2. If `audio_data` is binary/base64 (real), transcribes it.
    
    Current implementation assumes text input for prototype simplicity 
    or until binary handling is added to WebSocket.
    """
    # Check if simulation (input is already text)
    if not is_base64(audio_data):
        return audio_data

    # Real Audio Processing (Stub for future binary implementation)
    # response = openai.Audio.transcribe("whisper-1", audio_file)
    return "Audio processing not yet implemented for binary data"

def is_base64(s: str) -> bool:
    # Simple heuristic to detect if simulation text or real audio data
    return len(s) > 100 and " " not in s[:50]

