import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import PyPDF2
from tqdm import tqdm
import pickle
 
def initialize_faiss(index_file: str):
    """Initialize FAISS and return index and model"""
    # Initialize embedding model
    model = SentenceTransformer('all-MiniLM-L6-v2')  # 384 dimensions
    # Load or create FAISS index
    dimension = 384  # MiniLM model dimension
    if os.path.exists(index_file):
        with open(index_file, "rb") as f:
            index = pickle.load(f)
    else:
        index = faiss.IndexFlatL2(dimension)
    return index, model
 
def save_faiss_index(index, index_file):
    """Save FAISS index to disk"""
    with open(index_file, "wb") as f:
        pickle.dump(index, f)
 
def upload_pdf(index, model, pdf_path: str, index_file: str):
    """Upload a PDF file to FAISS"""
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
        # Convert embeddings to FAISS format
        vectors = np.array(embeddings, dtype='float32')
        # Add to FAISS index
        index.add(vectors)
        # Save updated index
        save_faiss_index(index, index_file)
        print(f"Successfully uploaded {pdf_path}")
        return True
    except Exception as e:
        print(f"Error uploading PDF: {str(e)}")
        return False
 
# Usage example:
if __name__ == "__main__":
    INDEX_FILE = "faiss_index.pkl"
    # Initialize FAISS
    index, model = initialize_faiss(INDEX_FILE)
    # Upload PDF
    pdf_path = "your_document.pdf"
    upload_pdf(index, model, pdf_path, INDEX_FILE)