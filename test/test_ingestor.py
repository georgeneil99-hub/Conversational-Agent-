import sys
import os

# 1. Add the workspace root to sys.path so 'src' can be found
# This assumes test_ingestor.py is in /workspaces/Conversational-Agent-/test/
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root_dir)

# 2. Import the function from the ingestor module
try:
    from src.ingestor import ingest_all_data
    print("✅ Successfully imported ingest_all_data")
except ImportError as e:
    print(f"❌ Import Error: {e}")
    sys.exit(1)

def test_loading():
    print("--- Starting Data Ingestion Test ---")
    
    # 3. Pathing for the data folder
    # If running from root, use "data/". If from test folder, use "../data/"
    data_path = os.path.join(root_dir, "data")
    
    # Call the function defined in ingestor.py [cite: 82-105]
    docs = ingest_all_data(data_dir=data_path)
    
    if not docs:
        print(f"Error: No documents found in {data_path}")
        return

    print(f"Success: Loaded {len(docs)} chunks.")
    print(f"Sample Content: {docs[0].page_content[:50]}...")

if __name__ == "__main__":
    test_loading()