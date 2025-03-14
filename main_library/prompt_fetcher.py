from pymongo import MongoClient
from flask import jsonify


# Connect to MongoDB
client = MongoClient("mongodb://127.0.0.1:27017/")
db = client["ChatBot"]
collection = db["prompts"]


def get_prompts():
    try:
        # Fetch all documents excluding `_id`
        documents = list(collection.find({}, {"_id": 0}))
        return {"result": documents}  # Return a dictionary, not a Response
        
    except Exception as e:
        return {"error": str(e)}  # Return error as a dictionary