from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

class AstroVectorStore:
    def __init__(self):
        self.vector_db = None
        self.embeddings = OpenAIEmbeddings()

    def initialize_vector_db(self, documents):
        """Builds the FAISS index from processed chunks."""
        self.vector_db = FAISS.from_documents(documents, self.embeddings)
        print("Vector database initialized.")

    def is_retrieval_required(self, query: str) -> bool:
        """
        Explicitly decides when to retrieve[cite: 89].
        Returns True for factual/astrological queries.
        Returns False for greetings, summaries, or follow-ups[cite: 94, 95].
        """
        retrieval_keywords = ["why", "planet", "career", "love", "future", "affecting", "traits"]
        query_lower = query.lower()
        
        # Simple keyword check or a small LLM 'intent' check
        if any(word in query_lower for word in retrieval_keywords):
            return True
        return False

    def get_relevant_context(self, query: str):
        """Fetches facts from vedic_astrology.txt or JSON files [cite: 103-105]."""
        if not self.vector_db:
            return []
        
        # Search for the top 3 most relevant snippets
        search_results = self.vector_db.similarity_search(query, k=3)
        return search_results