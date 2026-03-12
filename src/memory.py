from langchain.memory import ConversationBufferWindowMemory
from typing import Dict

class AstroMemoryManager:
    def __init__(self):
        # Dictionary to maintain separate state for each session_id 
        self.sessions: Dict[str, ConversationBufferWindowMemory] = {}
        # Persistent storage for profiles linked to sessions [cite: 86]
        self.user_profiles: Dict[str, dict] = {}

    def get_session_memory(self, session_id: str):
        """Implements session-based multi-turn memory (not stateless)."""
        if not session_id:
            return None
            
        if session_id not in self.sessions:
            # k=5 implements 'Last-N turns' for controlled memory growth [cite: 99-100]
            self.sessions[session_id] = ConversationBufferWindowMemory(
                k=5, 
                return_messages=True,
                memory_key="chat_history"
            )
        return self.sessions[session_id]

    def add_exchange(self, session_id: str, user_input: str, ai_output: str):
        """Saves the conversation turn to the persistent profile[cite: 86]."""
        memory = self.get_session_memory(session_id)
        if memory:
            memory.save_context({"input": user_input}, {"output": ai_output})

    def get_history(self, session_id: str) -> str:
        """Retrieves history for contextual reasoning[cite: 87, 115]."""
        memory = self.get_session_memory(session_id)
        if not memory:
            return ""
            
        messages = memory.load_memory_variables({})["chat_history"]
        # Formats history to allow the LLM to summarize previous turns [cite: 94, 99]
        return "\n".join([f"{'User' if m.type=='human' else 'AI'}: {m.content}" for m in messages])

    def store_user_profile(self, session_id: str, profile: dict):
        """Keeps birth details persistent across the session[cite: 85, 86]."""
        self.user_profiles[session_id] = profile