import os
from fastapi import FastAPI, HTTPException
from .models import ChatRequest, ChatResponse, calculate_zodiac
from .ingestor import ingest_all_data
from .vector_store import AstroVectorStore
from .memory import AstroMemoryManager

app = FastAPI(title="Astro Agent - Mock Mode")

# Global instances
vector_store = AstroVectorStore()
memory_manager = AstroMemoryManager()

@app.on_event("startup")
async def startup_event():
    """Ingests the mock corpus from the data/ directory [cite: 102-105]."""
    docs = ingest_all_data()
    vector_store.initialize_vector_db(docs)

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        session_id = request.session_id
        user_query = request.message
        profile = request.user_profile
        
        # Determine Mandatory Zodiac [cite: 107]
        zodiac = calculate_zodiac(profile.birth_date)
        
        # Intent-Aware Retrieval Decision [cite: 101-102]
        should_retrieve = vector_store.is_retrieval_required(user_query)
        context_used = []
        context_text = ""
        
        if should_retrieve:
            docs = vector_store.get_relevant_context(user_query)
            context_used = [doc.metadata.get("source", "unknown") for doc in docs]
            context_text = " ".join([d.page_content for d in docs])
        
        # Retrieval Logic: One case where it helps/hurts 
        # MOCK LLM LOGIC: Simulates a response using the context
        ai_response = (
            f"Hello {profile.name}. As a {zodiac} from {profile.birth_place}, "
            f"I have analyzed your query: '{user_query}'. "
        )
        if should_retrieve:
            ai_response += f"Based on {context_used[0] if context_used else 'Vedic texts'}, I suggest focusing on your inner energy."
        else:
            ai_response += "I'm remembering our previous conversation to provide this summary."

        # Update Session Memory [cite: 99]
        memory_manager.update_memory(session_id, user_query, ai_response)
        
        return ChatResponse(
            response=ai_response,
            zodiac=zodiac,
            context_used=context_used,
            retrieval_used=should_retrieve
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))