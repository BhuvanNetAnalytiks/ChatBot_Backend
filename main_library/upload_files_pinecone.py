import os
import pinecone
from sentence_transformers import SentenceTransformer
import PyPDF2
from tqdm import tqdm

def initialize_pinecone(api_key: str, environment: str):
    """Initialize Pinecone and return index"""
    # Initialize Pinecone
    pinecone.init(api_key=api_key, environment=environment)
    
    # Initialize embedding model
    model = SentenceTransformer('all-MiniLM-L6-v2')  # 384 dimensions
    
    # Create or get index
    index_name = "pdf-store"
    if index_name not in pinecone.list_indexes():
        pinecone.create_index(
            name=index_name,
            dimension=384,  # MiniLM model dimension
            metric="cosine"
        )
    
    index = pinecone.Index(index_name)
    return index, model

def upload_pdf(index, model, pdf_path: str):
    """Upload a PDF file to Pinecone"""
    try:
        # Extract text from PDF
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
        
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
        
        # Upload chunks to Pinecone
        print(f"Uploading {len(processed_chunks)} chunks...")
        batch_size = 100
        
        for i in tqdm(range(0, len(processed_chunks), batch_size)):
            batch_chunks = processed_chunks[i:i + batch_size]
            
            # Create embeddings for the batch
            embeddings = model.encode(batch_chunks)
            
            # Prepare vectors for Pinecone
            vectors = []
            for j, (chunk, embedding) in enumerate(zip(batch_chunks, embeddings)):
                vectors.append((
                    f"{os.path.basename(pdf_path)}_{i + j}",  # Vector ID
                    embedding.tolist(),  # Convert numpy array to list
                    {
                        "text": chunk,
                        "source": pdf_path
                    }
                ))
            
            # Upsert to Pinecone
            index.upsert(vectors=vectors)
        
        print(f"Successfully uploaded {pdf_path}")
        return True
        
    except Exception as e:
        print(f"Error uploading PDF: {str(e)}")
        return False

# Usage example:
if __name__ == "__main__":
    # Initialize Pinecone
    PINECONE_API_KEY = "your-api-key"
    PINECONE_ENV = "your-environment"  # e.g., "gcp-starter"
    
    index, model = initialize_pinecone(PINECONE_API_KEY, PINECONE_ENV)
    
    # Upload PDF
    pdf_path = "your_document.pdf"
    upload_pdf(index, model, pdf_path)