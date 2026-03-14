import json
import os

class AstroDocument:
    """
    Simplified Document object to replace LangChain's native class.
    Added 'id' attribute to ensure compatibility with FAISS.from_documents.
    """
    def __init__(self, page_content, metadata, doc_id=None):
        self.page_content = page_content
        self.metadata = metadata
        self.id = doc_id  # Fixes: AttributeError: 'AstroDocument' object has no attribute 'id'

def read_file(file_path):
    file_ext = os.path.splitext(file_path)[1].lower()
    documents = []
    
    try:
        if file_ext == '.json':
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            for key, value in data.items():
                content = f"Key: {key}\nDetails: {json.dumps(value)}"
                documents.append(AstroDocument(content, {"source": file_path}))
        
        elif file_ext == '.txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            # Simple paragraph-based chunking
            chunks = text.split('\n\n')
            for chunk in chunks:
                if chunk.strip():
                    documents.append(AstroDocument(chunk.strip(), {"source": file_path}))
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        
    return documents

def ingest_all_data(data_dir="data/"):
    all_docs = []
    required_files = ['vedic_astrology.txt', 'planetary_traits.json', 'zodiac_personality.json']
    
    for file_name in required_files:
        full_path = os.path.join(data_dir, file_name)
        if os.path.exists(full_path):
            docs = read_file(full_path)
            all_docs.extend(docs)
    return all_docs