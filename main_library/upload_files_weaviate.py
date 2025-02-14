import weaviate
from sentence_transformers import SentenceTransformer
import PyPDF2
from typing import List
from tqdm import tqdm
import uuid

def initialize_weaviate():
    """Initialize Weaviate client and create schema"""
    # Initialize client
    client = weaviate.Client("http://localhost:8080")
    
    # Initialize embedding model
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Create schema if it doesn't exist
    schema = {
        "classes": [{
            "class": "Document",
            "vectorizer": "none",
            "properties": [
                {
                    "name": "content",
                    "dataType": ["text"]
                },
                {
                    "name": "source",
                    "dataType": ["string"]
                }
            ]
        }]
    }
    
    # Check and create schema
    try:
        existing_schema = client.schema.get()
        if not any(cls['class'] == 'Document' for cls in existing_schema['classes']):
            client.schema.create_class(schema['classes'][0])
    except:
        client.schema.create(schema)
    
    return client, model

def upload_pdf(client, model, pdf_path: str):
    """Upload a PDF file to Weaviate"""
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
        
        # Upload chunks to Weaviate
        print(f"Uploading {len(processed_chunks)} chunks...")
        with client.batch as batch:
            batch.batch_size = 100
            for chunk in tqdm(processed_chunks):
                # Create embedding
                embedding = model.encode(chunk)
                
                # Add to Weaviate
                batch.add_data_object(
                    data_object={
                        "content": chunk,
                        "source": pdf_path
                    },
                    class_name="Document",
                    vector=embedding.tolist(),
                    uuid=uuid.uuid4()
                )
        
        print(f"Successfully uploaded {pdf_path}")
        return True
        
    except Exception as e:
        print(f"Error uploading PDF: {str(e)}")
        return False

# Usage example:
if __name__ == "__main__":
    # Initialize
    client, model = initialize_weaviate()
    
    # Upload PDF
    pdf_path = "your_document.pdf"
    upload_pdf(client, model, pdf_path) 