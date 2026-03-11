# Conversational-Agent-
Astro Conversational Insight Agent — RAG + Conversation Ownership , 
📝 Astro Conversational Insight Agent — RAG + Conversation Ownership 
Problem Statement
Build a multi-turn conversational AI service that:
Takes user birth details (name, DOB, time, location)


Builds a persistent user profile


Answers multi-turn astrology questions with contextual reasoning


Uses retrieval-augmented generation (RAG) to ground responses in astrological knowledge


Makes explicit decisions on when to retrieve and when not to


Example User Questions
“Why is today stressful for me?”


“What should I focus on in my career this month?”


“Which planet is affecting my love life?”


“Summarize what you’ve told me so far”


“Why are you saying this again?”


🎯 Key Goals 
You are expected to demonstrate:
Conversation state ownership


Memory across turns/conversations (Last-N turns or simple summarization is sufficient)
Controlled memory growth


Intent-aware RAG


Retrieval only when it adds value
Retrieve facts from a mock knowledge corpus like:
data/vedic_astrology.txt 
data/planetary_traits.json
data/zodiac_personality.json
Personalization


Zodiac sign (mandatory)
Bonus: moon sign / age / goals (stubs acceptable)


Quality & cost awareness


Basic evaluation approach 
one case where retrieval helped
one case where retrieval hurt
Thoughtful trade-offs



🧱 Minimum Required Architecture (Tightened)
Layer
Requirement
API Layer
FastAPI / Flask — /chat POST
Conversation Layer
Session-based multi-turn memory (not stateless)
LLM Layer
Model abstraction (OpenAI / local / stub)
Retrieval Layer
Semantic embeddings + vector search (FAISS / ChromaDB)
Retrieval Logic
Intent-aware (not always-on)
Memory Control
Windowing / summarization / decay
Language
Hindi toggle supported
Error Handling
Validation, retries, safe fallbacks


📌 API Contract (Same shape, stricter semantics)
Input
{
  "session_id": "abc-123",
  "message": "How will my month be in career?",
  "user_profile": {
    "name": "Ritika",
    "birth_date": "1995-08-20",
    "birth_time": "14:30",
    "birth_place": "Jaipur, India",
    "preferred_language": "hi"
  }
}

Output
{
  "response": "आपके लिए यह महीना अवसर लेकर आ रहा है...",
  "zodiac": "Leo",
  "context_used": ["career_guidance", "leo_traits"],
  "retrieval_used": true
}

