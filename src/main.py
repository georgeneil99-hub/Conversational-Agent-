import os
from fastapi import FastAPI, HTTPException
from .models import ChatRequest, ChatResponse, calculate_zodiac
from .ingestor import ingest_all_data
from .vector_store import AstroVectorStore
from .memory import AstroMemoryManager

app = FastAPI(title="Astro Conversational Insight Agent")

# Global instances initialized once
vector_store = AstroVectorStore()
memory_manager = AstroMemoryManager()

@app.on_event("startup")
async def startup_event():
    """Ingests the mock corpus from the data/ directory [cite: 102-105]."""
    # Use absolute path to ensure reliability in different environments
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_path, "data")
    docs = ingest_all_data(data_dir=data_path)
    vector_store.initialize_vector_db(docs)


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        session_id = request.session_id
        user_query = request.message
        profile = request.user_profile
        
        # 1. Persist User Profile for the session [cite: 86]
        memory_manager.store_user_profile(session_id, profile.dict())
        
        # 2. Mandatory Personalization [cite: 107]
        zodiac = calculate_zodiac(profile.birth_date)
        
        # 3. Intent-Aware Retrieval [cite: 101-102]
        should_retrieve = vector_store.is_retrieval_required(user_query)
        context_used = []
        if should_retrieve:
            docs = vector_store.get_relevant_context(user_query)
            context_used = [doc.metadata.get("source", "unknown") for doc in docs]

        # 4. Access Multi-turn History [cite: 99]
        # This allows answering: "Summarize what you told me so far"
        history = memory_manager.get_history(session_id)
        
        # 5. Mock AI Logic with Contextual Reasoning [cite: 87]
        ai_response = f"Hello {profile.name}. Based on your birth details in {profile.birth_place}..."
        if "summarize" in user_query.lower():
            ai_response = f"So far, we have discussed: {history if history else 'nothing yet'}."

        # 6. Save current exchange 
        memory_manager.add_exchange(session_id, user_query, ai_response)
        
        return ChatResponse(
            response=ai_response,
            zodiac=zodiac,
            context_used=context_used,
            retrieval_used=should_retrieve
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))