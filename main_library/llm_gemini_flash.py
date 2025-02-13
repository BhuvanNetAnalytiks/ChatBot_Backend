import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def query_gemini_llm(question, context):
    """Enhanced Gemini prompt for more focused answers"""

    model = genai.GenerativeModel('gemini-1.5-flash')

    prompt = f"""
    Based on the following context, please provide a direct and concise answer to the question.
    If the answer isn't found in the context, please say so.
    Question: {question}
    Context: {context}
    Please provide a clear, focused answer to the question using only information from the context. If the answer isn't in the context, say "I cannot find information about that in the available documents."
    Answer: """

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error generating LLM response: {e}")
        return "I apologize, but I encountered an error processing your question. Please try again."