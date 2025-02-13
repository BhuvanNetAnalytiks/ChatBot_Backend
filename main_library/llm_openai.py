import os
import openai

# Set API key
openai.api_key = os.getenv("OPENAI_API_KEY") 

def query_openai_llm(question, context):
    """Enhanced OpenAI GPT prompt for more focused answers"""
    
    prompt = f"""
    Based on the following context, please provide a direct and concise answer to the question.
    If the answer isn't found in the context, please say so.
    
    Question: {question}
    
    Context: {context}
    
    Please provide a clear, focused answer to the question using only information from the context. If the answer isn't in the context, say "I cannot find information about that in the available documents."
    
    Answer: """
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[{"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": prompt}],
            temperature=0
        )
        return response["choices"][0]["message"]["content"].strip()
    
    except Exception as e:
        print(f"Error generating LLM response: {e}")
        return "I apologize, but I encountered an error processing your question. Please try again."

