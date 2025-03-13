import google.generativeai as genai
import os
# from dotenv import load_dotenv
# load_dotenv('key.env')

genai.configure(api_key="AIzaSyAwgKHTpiDagE8MvbC6WuHZ5n1i7yz5pEk")

def query_gemini_llm(question, context):
    """Enhanced Gemini prompt for more focused answers"""

    model = genai.GenerativeModel('gemini-1.5-flash')

    # prompt = f"""
    # Based on the following context, please provide a direct and concise answer to the question.
    # If the answer isn't found in the context, please say so.
    # Question: {question}
    # Context: {context}
    # Please provide a clear and focused answer to the question using only the information available in the provided context. 
    # If the answer is not found in the context, generate an answer using your knowledge base.
    # Answer: """
    prompt = f"""
        Based on the following context retrieved from the Milvus database, please provide a direct and concise answer to the question.
        If the answer is found in the context rephrase the answer before responding, respond with:
        Knowledgebase response: "<answer>"
        If the answer isn't found in the context, generate an answer using your knowledge base and respond with:
        LLM response: "<answer>"
        Question: {question}
        Context: {context}
   
        Answer: """

    try:
        response = model.generate_content(prompt)
        return response.text.strip()

    except Exception as e:
        print(f"Error generating LLM response: {e}")
        return "I apologize, but I encountered an error processing your question. Please try again."