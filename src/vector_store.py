import os
import faiss
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

class AstroVectorStore:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        # Load local embedding model
        self.embeddings = HuggingFaceEmbeddings(model_name=model_name)
        self.vector_db = None

    def initialize_vector_db(self, documents, index_path="faiss_index"):
        """
        Builds or loads the FAISS index.
        Uses from_texts to avoid ID-related attribute errors.
        """
        if os.path.exists(index_path):
            print(f"--- Loading existing index from {index_path} ---")
            self.vector_db = FAISS.load_local(
                index_path, 
                self.embeddings, 
                allow_dangerous_deserialization=True
            )
        elif documents:
            print("--- Creating new FAISS index from documents ---")
            texts = [doc.page_content for doc in documents]
            metadatas = [doc.metadata for doc in documents]
            
            # Using from_texts is the most stable way to handle custom objects
            self.vector_db = FAISS.from_texts(
                texts=texts, 
                embedding=self.embeddings, 
                metadatas=metadatas
            )
            self.vector_db.save_local(index_path)
            print(f"--- Index saved to {index_path} ---")
        else:
            print("No documents available and no local index found.")

    def is_retrieval_required(self, query: str) -> bool:
        """Intent-aware logic: only retrieve for astrology-specific queries."""
        query_lower = query.lower()
        keywords = ["zodiac", "planet", "trait", "career", "future", "affect", "sun", "moon", "mars", "saturn"]
        return any(word in query_lower for word in keywords)

    def get_relevant_context(self, query: str, k=3):
        if not self.vector_db:
            return []
        return self.vector_db.similarity_search(query, k=k)