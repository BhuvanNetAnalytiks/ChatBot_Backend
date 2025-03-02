from sentence_transformers import SentenceTransformer
from pymilvus import connections, Collection
from dotenv import load_dotenv
import os
import google.generativeai as genai
from main_library.llm_gemini_flash import query_gemini_llm

# Load environment variables from .env file
load_dotenv()

# Load the sentence transformer model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
MILVUS_HOST = 'localhost'
MILVUS_PORT = '19530'
MILVUS_ALIAS = 'default'


 
def setup_milvus_connection():
    """ Setup the Milvus connection """
    try:
        connections.connect(
            alias=MILVUS_ALIAS,
            host=MILVUS_HOST,
            port=MILVUS_PORT
        )
        print("✅ Connected to Milvus Successfully")
    except Exception as e:
        print(f"❌ Error: Failed to connect to Milvus: {str(e)}")
 
def ensure_milvus_connection():
    """ Ensure Milvus is connected before performing any operations. """
    if not connections.has_connection(alias=MILVUS_ALIAS):
        setup_milvus_connection()
 
def generate_embedding(text):
    """Generate an embedding for the given text."""
    try:
        return model.encode(text)
    except Exception as e:
        return f"Error generating embedding: {str(e)}"
 
 
def semantic_search_and_answer(question, department=None):
    top_k=3
    # Ensure Milvus connection is active
    setup_milvus_connection()
    if not connections.has_connection(alias=MILVUS_ALIAS):
        setup_milvus_connection()
    # Check again to be sure the connection was established
    if not connections.has_connection(alias=MILVUS_ALIAS):
        return "Milvus connection could not be established."
 
    if not department:
        return "No department specified for searching documents."
    
    collection_name = f"{department.lower()}_collection"
    
    try:
        # Get collection and load it
        collection = Collection(name=collection_name)
        collection.load()
        
        # Generate embedding for the question
        question_embedding = generate_embedding(question)
        
        # Search parameters
        search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
        
        # Perform search
        results = collection.search(
            data=[question_embedding.tolist()],
            anns_field="embedding",
            param=search_params,
            limit=top_k,
            output_fields=["content"]
        )
        
        if not results or not results[0]:
            return f"No relevant information found in {department} department documents."
        
        # Extract content from results
        contexts = []
        for hits in results:
            for hit in hits:
                try:
                    content = str(hit.fields['content'])
                    if content and content.strip():
                        contexts.append(content)
                except (KeyError, AttributeError) as e:
                    print(f"Error accessing hit content: {e}")
                    continue
        
        if not contexts:
            return f"No readable content found in {department} department documents."
        
        combined_context = " ".join(contexts)
        
        answer = query_gemini_llm(question, combined_context)
        return answer
    
    except Exception as e:
        print(f"Error in semantic search for {department} department: {e}")
        return f"An error occurred while searching {department} department documents."
 
 