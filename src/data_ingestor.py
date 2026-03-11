import json
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

def read_file(file_path):
    """
    Ingests and processes data based on file extension.
    Returns a list of LangChain Document objects ready for vectorization.
    """
    file_ext = os.path.splitext(file_path)[1].lower()
    
    try:
        if file_ext == '.json':
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # For JSON, we convert each entry into a document string
            # This is critical for planetary_traits and zodiac_personality
            documents = []
            for key, value in data.items():
                content = f"Key: {key}\nDetails: {json.dumps(value)}"
                documents.append(Document(page_content=content, metadata={"source": file_path, "type": "structured"}))
            return documents

        elif file_ext == '.txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            # Recursive splitting preserves paragraph/sentence integrity 
            # Essential for long astrological texts like vedic_astrology.txt
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=800,
                chunk_overlap=100,
                separators=["\n\n", "\n", " ", ""]
            )
            return text_splitter.create_documents([text], metadatas=[{"source": file_path, "type": "unstructured"}])
        
        else:
            print(f"Unsupported file format: {file_ext}")
            return []

    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return []

def ingest_all_data(data_dir="data/"):
    """
    Loops through the data directory and processes all required files.
    """
    all_docs = []
    required_files = ['vedic_astrology.txt', 'planetary_traits.json', 'zodiac_personality.json']
    
    for file_name in required_files:
        full_path = os.path.join(data_dir, file_name)
        if os.path.exists(full_path):
            docs = read_file(full_path)
            all_docs.extend(docs)
            print(f"Successfully processed {len(docs)} chunks from {file_name}")
            
    return all_docs