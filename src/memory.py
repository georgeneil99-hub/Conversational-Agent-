from langchain.memory import ConversationBufferWindowMemory
from typing import Dict

class AstroMemoryManager:
    def __init__(self):
        # Dictionary to store memory objects per session_id
        self.sessions: Dict[str, ConversationBufferWindowMemory] = {}

    def get_session_memory(self, session_id: str):
        """
        Retrieves or creates a session-based multi-turn memory.
        Uses k=5 to implement 'Last-N turns' controlled growth.
        """
        if session_id not in self.sessions:
            # k=5 ensures memory doesn't grow indefinitely (Memory Control)
            self.sessions[session_id] = ConversationBufferWindowMemory(
                k=5, 
                return_messages=True,
                memory_key="chat_history"
            )
        return self.sessions[session_id]

    def get_history_as_string(self, session_id: str) -> str:
        """Returns the conversation history formatted for the LLM prompt."""
        memory = self.get_session_memory(session_id)
        messages = memory.load_memory_variables({})["chat_history"]
        
        history_text = ""
        for msg in messages:
            prefix = "User: " if msg.type == "human" else "Assistant: "
            history_text += f"{prefix}{msg.content}\n"
        return history_text

    def update_memory(self, session_id: str, user_input: str, ai_output: str):
        """Adds the latest exchange to the persistent user profile state."""
        memory = self.get_session_memory(session_id)
        memory.save_context({"input": user_input}, {"output": ai_output})