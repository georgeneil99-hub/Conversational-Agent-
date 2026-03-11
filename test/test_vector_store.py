import sys
import os

# 1. Add workspace root to path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root_dir)

from src.ingestor import ingest_all_data
from src.vector_store import AstroVectorStore

def test_retrieval():
    print("--- Starting Vector Store & Retrieval Test ---")
    
    # Initialize components
    vector_store = AstroVectorStore()
    data_path = os.path.join(root_dir, "data")
    
    # 2. Load data and initialize DB
    print("Ingesting data from:", data_path)
    docs = ingest_all_data(data_dir=data_path)
    if not docs:
        print("❌ Error: No documents found to index.")
        return
        
    vector_store.initialize_vector_db(docs)
    
    # 3. Test Intent-Aware Logic 
    queries = [
        ("What are Leo traits?", True),       # Should require retrieval
        ("Hello, how are you?", False),       # Should NOT require retrieval
        ("Tell me about Saturn", True)        # Should require retrieval
    ]
    
    for query, expected in queries:
        decision = vector_store.is_retrieval_required(query)
        status = "✅" if decision == expected else "❌"
        print(f"{status} Query: '{query}' | Retrieval Required: {decision}")

    # 4. Test Semantic Search Quality [cite: 47, 88]
    print("\n--- Testing Semantic Search ---")
    test_query = "Tell me about Leo personality"
    results = vector_store.get_relevant_context(test_query)
    
    if results:
        print(f"✅ Success: Found {len(results)} relevant snippets.")
        print(f"Top Result Source: {results[0].metadata.get('source')}")
        print(f"Top Result Content: {results[0].page_content[:100]}...")
    else:
        print("❌ Error: Search returned no results.")

if __name__ == "__main__":
    test_retrieval()