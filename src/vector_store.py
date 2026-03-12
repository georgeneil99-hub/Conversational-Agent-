from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings # No API key needed
import logging

logger = logging.getLogger(__name__)

class AstroVectorStore:
    def __init__(self):
        self.vector_db = None
        # Using a lightweight local model: sentence-transformers/all-MiniLM-L6-v2
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    def initialize_vector_db(self, documents):
        """Builds the FAISS index from the documents loaded by ingestor.py."""
        if not documents:
            logger.error("No documents provided to initialize Vector DB.")
            return
        self.vector_db = FAISS.from_documents(documents, self.embeddings)
        logger.info("Local FAISS Vector DB initialized successfully.")

    def is_retrieval_required(self, query: str) -> bool:
        query_lower = query.lower()
        # Add common planets to the intent keywords
        keywords = [
            "zodiac", "planet", "trait", "career", "stress", "future", "affect",
            "sun", "moon", "mars", "mercury", "jupiter", "venus", "saturn"
        ]
        return any(word in query_lower for word in keywords)

    def get_relevant_context(self, query: str):
        """Performs semantic search to find top-3 relevant facts[cite: 47, 88]."""
        if not self.vector_db:
            return []
        # Return top 3 matches for grounding responses [cite: 102]
        return self.vector_db.similarity_search(query, k=3)