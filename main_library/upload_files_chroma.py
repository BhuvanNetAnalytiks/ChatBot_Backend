import os
import chromadb
from sentence_transformers import SentenceTransformer
import PyPDF2
from tqdm import tqdm
 
def initialize_chroma(db_path: str):
    """Initialize ChromaDB and return collection and model"""
    # Initialize embedding model
    model = SentenceTransformer('all-MiniLM-L6-v2')  # 384 dimensions
    # Initialize Chroma client
    client = chromadb.PersistentClient(path=db_path)
    collection = client.get_or_create_collection(name="pdf_store")
    return collection, model
 
def upload_pdf(collection, model, pdf_path: str):
    """Upload a PDF file to ChromaDB"""
    try:
        # Extract text from PDF
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = "".join([page.extract_text() for page in pdf_reader.pages])
        # Split text into chunks
        chunks = text.split('. ')
        chunk_size = 1000
        processed_chunks = []
        current_chunk = ""
        for chunk in chunks:
            if len(current_chunk) + len(chunk) < chunk_size:
                current_chunk += chunk + ". "
            else:
                processed_chunks.append(current_chunk)
                current_chunk = chunk + ". "
        if current_chunk:
            processed_chunks.append(current_chunk)
        # Create embeddings for chunks
        print(f"Uploading {len(processed_chunks)} chunks...")
        embeddings = model.encode(processed_chunks)
        # Add to ChromaDB collection
        for i, (chunk, embedding) in enumerate(zip(processed_chunks, embeddings)):
            collection.add(
                ids=[f"{os.path.basename(pdf_path)}_{i}"],
                embeddings=[embedding.tolist()],
                metadatas=[{"text": chunk, "source": pdf_path}]
            )
        print(f"Successfully uploaded {pdf_path}")
        return True
    except Exception as e:
        print(f"Error uploading PDF: {str(e)}")
        return False
 
# Usage example:
if __name__ == "__main__":
    DB_PATH = "chroma_db"
    # Initialize ChromaDB
    collection, model = initialize_chroma(DB_PATH)
    # Upload PDF
    pdf_path = "your_document.pdf"
    upload_pdf(collection, model, pdf_path)

