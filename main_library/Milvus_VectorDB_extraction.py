from sentence_transformers import SentenceTransformer
from pymilvus import connections, Collection
from dotenv import load_dotenv
import os 

# Load environment variables from .env file
load_dotenv()

# Load the sentence transformer model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
MILVUS_HOST = os.getenv("MILVUS_HOST")
MILVUS_PORT = os.getenv("MILVUS_PORT")
MILVUS_ALIAS = os.getenv("MILVUS_ALIAS")


def setup_milvus_connection():
    """ Setup the Milvus connection and create a collection """
    try:
        connections.connect(
            host = MILVUS_HOST,
            port = MILVUS_PORT,
            alias = MILVUS_ALIAS
        )
        return "Connected to Milvus Successfully"
    except Exception as e:
        return f"error: Failed to connect to Milvus: {str(e)}"

def ensure_milvus_connection():
    """ Ensure the Milvus is connected before performing any operations. """
    try:
        if not connections.connect(alias = MILVUS_ALIAS):
            return setup_milvus_connection()
    except Exception as e:
        return {"error": f"Failed to connect to Milvus: {str(e)}"}
    
def generate_embedding(text):
    """Generate an embedding for the given text."""
    try:
        return model.encode(text)
    except Exception as e:
        return f"Error generating embedding: {str(e)}"


def fetch_from_milvus(question, department, top_k=5):
    """
    Perform a semantic search in Milvus for a given question in a specified department.

    :param question: User's query
    :param department: Department name to search within
    :param top_k: Number of results to fetch
    :return: List of relevant document content or error message
    """
    if not department:
        return "Department not specified. Please provide a valid department."

    collection_name = f"{department.lower()}_collection"

    connection_status = ensure_milvus_connection()
    if connection_status:
        return connection_status

    try:
        collection = Collection(name=collection_name)
        collection.load()

        # Generate embedding for the question
        question_embedding = generate_embedding(question)
        if isinstance(question_embedding, str):  # If an error message is returned
            return question_embedding

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
            return f"No relevant information found in {department} department."

        # Extract content from search results
        contexts = []
        for hits in results:
            for hit in hits:
                content = str(hit.fields.get('content', ''))
                if content.strip():
                    contexts.append(content)

        if not contexts:
            return f"No readable content found in {department} department documents."

        return contexts

    except Exception as e:
        return f"Error in semantic search for {department} department: {str(e)}"
    


# Initialize Milvus Connection
# setup_milvus_connection()    