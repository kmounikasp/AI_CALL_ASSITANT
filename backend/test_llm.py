import os
import asyncio
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

async def test_connectivity():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("OPENAI_API_KEY not found in .env")
        return

    print(f"Testing with API Key prefix: {api_key[:8]}...")
    client = AsyncOpenAI(api_key=api_key)
    
    try:
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello, respond with 'Connected'"}],
            max_tokens=10
        )
        print(f"LLM Response: {response.choices[0].message.content.strip()}")
    except Exception as e:
        print(f"API Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_connectivity())
