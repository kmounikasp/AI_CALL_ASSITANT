from typing import List
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.llm_service import analyze_sentiment, generate_sales_prompt, extract_keywords
from app.services.crm_service import get_product_recommendations
from app.services.session_manager import session_manager
from app.services.speech_service import process_audio_chunk

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket, session_id: str):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

manager = ConnectionManager()

@router.websocket("/ws/audio/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await manager.connect(websocket, session_id)
    try:
        while True:
            # Receive audio data (assuming text for simulation or bytes for real audio later)
            data = await websocket.receive_text() 
            
            # 1. Process Audio (or text)
            transcript = await process_audio_chunk(data)
            
            # Record transcript
            session_manager.add_to_transcript(session_id, transcript)
            
            # 2. Analyze Sentiment
            sentiment = await analyze_sentiment(transcript)
            
            # 3. Generate Prompt (if applicable)
            suggestion = await generate_sales_prompt(transcript, sentiment)
            
            # 4. Extract Keywords (Async)
            keywords = await extract_keywords(transcript)
            
            # 5. Get Recommendations
            recommendations = get_product_recommendations(keywords)
            
            # Send back response
            response = {
                "transcript": transcript,
                "sentiment": sentiment,
                "suggestion": suggestion,
                "keywords": keywords,
                "recommendations": recommendations
            }
            await websocket.send_json(response)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print(f"Client {session_id} disconnected")

@router.get("/call/{session_id}/summary")
async def get_summary(session_id: str):
    summary = await session_manager.generate_summary(session_id)
    return {"session_id": session_id, "summary": summary}
