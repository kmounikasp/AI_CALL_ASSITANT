import os
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = AsyncOpenAI(api_key=api_key) if api_key else None

async def analyze_sentiment(text: str) -> str:
    """
    Analyzes sentiment using LLM (if key exists) or Keyword Fallback.
    """
    if client:
        try:
            response = await client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Analyze the sentiment of the following sales call transcript. Return ONLY one word: Positive, Negative, or Neutral."},
                    {"role": "user", "content": text}
                ]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            if "insufficient_quota" in str(e):
                print("LLM Error: Insufficient Quota (OpenAI API credits exhausted). Falling back to keyword analysis.")
            else:
                print(f"LLM Error: {e}")
            
    # Fallback
    text_lower = text.lower()
    positive_words = ["good", "great", "love", "yes", "interested", "perfect", "thanks", "thank you", "best", "latest"]
    negative_words = ["bad", "hate", "no", "wrong", "expensive", "too much", "mad", "angry", "worst", "broken", "annoying", "frustrated"]
    
    if any(w in text_lower for w in positive_words):
        return "Positive"
    elif any(w in text_lower for w in negative_words):
        return "Negative"
    return "Neutral"

async def generate_sales_prompt(text: str, sentiment: str) -> str:
    """
    Generates a sales prompt or objection handling technique.
    """
    if client:
        try:
            response = await client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a sales coach assistance. Based on the customer's input and sentiment, suggest a short, actionable question or objection handling response for the sales rep to say next. Keep it under 20 words."},
                    {"role": "user", "content": f"Customer: {text}\nSentiment: {sentiment}"}
                ]
            )
            return response.choices[0].message.content.strip()
        except Exception:
            pass

    # Fallback Improvement
    text_lower = text.lower()
    if sentiment == "Negative":
        if "mad" in text_lower or "angry" in text_lower:
            return "Empathize: 'I can hear that you're frustrated. I'm here to solve this. What's the main issue?'"
        return "Ask: 'What are your main concerns regarding this feature?'"
    
    if "charger" in text_lower or "laptop" in text_lower:
        return "Ask: 'Which model is your laptop? I can check for compatible hardware right now.'"
    
    if sentiment == "Positive":
        return "Try closing: 'Shall we look at the pricing plans?'"
    else:
        return "Ask: 'How does your current solution handle this?'"

async def extract_keywords(text: str) -> list:
    """
    Extracts interesting sales keywords from text using LLM or fallback.
    """
    if client:
        try:
            response = await client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Extract key technical or sales-related nouns/topics from the following text that might match a product catalog. Return a comma-separated list of single words (e.g., charger, laptop, discount)."},
                    {"role": "user", "content": text}
                ]
            )
            return [k.strip().lower() for k in response.choices[0].message.content.split(",")]
        except Exception:
            pass

    # Expanded Fallback
    standard_keywords = ["price", "cost", "budget", "competitor", "contract", "discount", "timeline", "urgent", "decision", "charger", "laptop", "macbook", "enterprise", "startup"]
    found = [word for word in standard_keywords if word in text.lower()]
    return found
