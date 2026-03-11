import os
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv

# Import your local modules
from models import ChatRequest, ChatResponse, calculate_zodiac
from ingestor import ingest_all_data
from vector_store import AstroVectorStore
from memory import AstroMemoryManager

load_dotenv()
app = FastAPI(title="Astro Conversational Insight Agent")

# Global instances for the 3-hour assignment
vector_store = AstroVectorStore()
memory_manager = AstroMemoryManager()

@app.on_event("startup")
async def startup_event():
    """Initializes the Knowledge Corpus on startup [cite: 102-105]."""
    docs = ingest_all_data()
    vector_store.initialize_vector_db(docs)

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Main API endpoint implementing multi-turn logic and Intent-aware RAG.
    """
    try:
        session_id = request.session_id
        user_query = request.message
        profile = request.user_profile
        
        # 1. Determine Zodiac sign (Mandatory Personalization) [cite: 107, 132]
        zodiac = calculate_zodiac(profile.birth_date)
        
        # 2. Intent-Aware Retrieval Logic [cite: 101-102]
        should_retrieve = vector_store.is_retrieval_required(user_query)
        context_docs = []
        context_titles = []
        
        if should_retrieve:
            context_docs = vector_store.get_relevant_context(user_query)
            context_titles = [doc.metadata.get("source", "unknown") for doc in context_docs]
        
        # 3. Retrieve Session History (Conversation State Ownership) [cite: 98-99]
        history = memory_manager.get_history_as_string(session_id)
        
        # 4. Mock LLM Logic (Replace with actual LLM call) 
        # In a real scenario, use LangChain's LLMChain here
        ai_response = f"Hello {profile.name}, as a {zodiac}, I see that..."
        
        # 5. Update Memory (Controlled Growth) [cite: 100]
        memory_manager.update_memory(session_id, user_query, ai_response)
        
        # 6. Return Response matching API Contract [cite: 129-135]
        return ChatResponse(
            response=ai_response,
            zodiac=zodiac,
            context_used=context_titles,
            retrieval_used=should_retrieve
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)