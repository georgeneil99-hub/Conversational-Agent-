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


This README details the implementation of a production-grade Intent-Aware RAG (Retrieval-Augmented Generation) agent tailored for the "Astrology Tech" domain. It is designed to meet the specific technical requirements for the Lead ML Engineer - 3 role at MyNaksh, prioritizing mystical grounding, deep persona memory, and Indic-first NLU.## 1. Quick Start: Command Line Steps### PrerequisitesPython 3.10+Local LLM Hosting (Optional but recommended: Ollama with llama3 for low-latency inference).### SetupBash# Clone and enter directory
git clone https://github.com/your-repo/astro-conversational-agent.git
cd astro-conversational-agent

# Environment setup
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install dependencies
pip install fastapi uvicorn pydantic sentence-transformers faiss-cpu
### Running the ApplicationBash# Start the server (includes automatic data ingestion and indexing on first run)
python -m uvicorn src.main:app --reload
### Testing the AgentOpen a new terminal and run a sample POST request to test Intent-Aware Retrieval and Personalization:Bashcurl -X POST "http://127.0.0.1:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{
           "session_id": "test-session-001",
           "message": "How does Mars affect my career?",
           "user_profile": {
             "name": "Ritika",
             "birth_date": "1995-08-20",
             "birth_time": "14:30",
             "birth_place": "Jaipur, India",
             "preferred_language": "hi"
           }
         }'
## 2. Core Architectural Concepts (Interview Showcase)To excel in high-stakes Astrology Tech roles, this system shifts from standard "Model Scientist" thinking to "System Architect" logic.### A. Intent-Aware Retrieval (The "Router" Logic)Instead of a standard "Retrieve-Every-Time" linear flow, this system utilizes Selective Retrieval.Concept: Before querying the Vector DB (FAISS), the system uses an intent classifier to determine if a search is necessary.Optimization: For "Chit-chat" or requests like "Can you summarize our chat?", the system bypasses the vector search to reduce latency and API costs.Interview Insight: This addresses the Cost/Quality Awareness paradigm shift, ensuring FAISS is only queried when it adds factual value.### B. Deep Persona Memory ManagementStandard chatbots are often stateless; this agent owns the conversation state.Sliding Window Memory: Implements a deque with a maxlen=k to ensure controlled memory growth.State Ownership: Moves beyond simple "Last-N" turns by linking session IDs to persistent user profiles (DOB, Time, Location) to infer life goals and personality traits.Hybrid Approach: While the middle of long conversations can be summarized to avoid the "Lost-in-the-Middle" problem, the core system prompt and user profile are "pinned" to maintain the "Guru-shishya" decorum.### C. "Bharat-First" Multilingual NLUTreating Hindi and Indian dialects as core logic layers rather than secondary translations.Tokenization Nuances: Standard tokenizers have high "Fertility Rates" for Hindi (breaking one word into 6+ tokens), which exhausts context windows and inflates costs.Indic-First Logic: Designed to handle Code-Switching (Hinglish) and Vibhakti (case endings) where standard English-centric NLP fails.Grounding in "Truth": To prevent hallucinations in ritual or Sloka interpretations, the system employs Correctness Agents that validate outputs against verified scriptures like the Panchang.## 3. System Design Trade-offsFeatureChoiceJustificationVector DBLocal FAISSChosen over managed services (Pinecone) to eliminate network hop latency for sub-second orchestration.MemorySliding WindowPrevents the model from "forgetting" the user's core intent while managing token limits without the loss of nuance found in constant summarization.RAG vs. Fine-tuningRAGAstrology requires factual grounding in fresh planetary transits. RAG provides non-parametric memory that doesn't suffer from "catastrophic forgetting".## 4. Future Roadmap & ScalabilityHybrid Search: Combining FAISS semantic search with keyword-based BM25 for precise ritual/entity lookup.Infrastructure Orchestration: Moving from a single-model setup to a routing layer that batches prompts across OpenAI, Claude, and LLaMA based on query complexity.Symbolic Hybrid AI: Integrating a symbolic rule-based engine for mathematically certain astronomical events (planetary degrees) while using LLMs for unstructured interpretation.