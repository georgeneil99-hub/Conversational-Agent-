import os
from fastapi import FastAPI, HTTPException
from .models import ChatRequest, ChatResponse, calculate_zodiac
from .ingestor import ingest_all_data
from .vector_store import AstroVectorStore
from .memory import AstroMemoryManager

# 1. Initialize FastAPI FIRST
app = FastAPI(title="Astro Conversational Insight Agent")

# 2. Global instances
vector_store = AstroVectorStore()
memory_manager = AstroMemoryManager(k=5)  # Controlled memory growth

@app.on_event("startup")
async def startup_event():
    """Initializes the vector DB from mock corpus on startup."""
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_path, "data")
    
    # Ingest and initialize pure FAISS store
    docs = ingest_all_data(data_dir=data_path)
    vector_store.initialize_vector_db(docs)

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        session_id = request.session_id
        user_query = request.message
        profile = request.user_profile
        
        # 1. Mandatory Personalization
        zodiac = calculate_zodiac(profile.birth_date)
        memory_manager.store_user_profile(session_id, profile.dict())
        
        # 2. Intent-Aware Retrieval Logic
        context_text = ""
        context_sources = []
        should_retrieve = vector_store.is_retrieval_required(user_query)
        
        if should_retrieve:
            results = vector_store.get_relevant_context(user_query)
            context_text = "\n".join([r.page_content for r in results])
            context_sources = list(set([getattr(r, 'metadata', {}).get('source', 'unknown') for r in results]))

        # 3. Access Multi-turn History (Pure Python)
        history = memory_manager.get_history(session_id)
        
        # 4. Mock AI Reasoning (Satisfies assignment requirements)
        # In a production setup, you'd pass (context_text + history + user_query) to an LLM
        ai_response = f"Hello {profile.name}. Based on your birth details in {profile.birth_place} and your {zodiac} traits..."
        
        if "summarize" in user_query.lower():
            ai_response = f"So far, we have discussed the following:\n{history}" if history else "We haven't discussed anything yet!"

        # 5. Save exchange to Sliding Window Memory
        memory_manager.add_exchange(session_id, user_query, ai_response)
        
        return ChatResponse(
            response=ai_response,
            zodiac=zodiac,
            context_used=context_sources,
            retrieval_used=should_retrieve
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))