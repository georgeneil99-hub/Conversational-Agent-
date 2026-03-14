from collections import deque

class AstroMemoryManager:
    def __init__(self, k=5):
        """Maintains a sliding window of the last k exchanges."""
        self.sessions = {}
        self.k = k
        self.user_profiles = {}

    def store_user_profile(self, session_id, profile):
        self.user_profiles[session_id] = profile

    def add_exchange(self, session_id, user_input, ai_output):
        if session_id not in self.sessions:
            self.sessions[session_id] = deque(maxlen=self.k)
        
        self.sessions[session_id].append({
            "user": user_input,
            "ai": ai_output
        })

    def get_history(self, session_id):
        if session_id not in self.sessions:
            return ""
        
        history_lines = [f"User: {t['user']}\nAI: {t['ai']}" for t in self.sessions[session_id]]
        return "\n\n".join(history_lines)