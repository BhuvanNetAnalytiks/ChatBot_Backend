import os
import anthropic

# Set up the Claude client
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))  # Fetch API key from env variable

def query_claude_llm(question, context):
    """Enhanced Claude prompt for more focused answers"""

    prompt = f"""
    Based on the following context, please provide a direct and concise answer to the question.
    If the answer isn't found in the context, please say so.

    Question: {question}

    Context: {context}

    Please provide a clear, focused answer to the question using only information from the context. 
    If the answer isn't in the context, say "I cannot find information about that in the available documents."

    Answer:
    """

    try:
        response = client.messages.create(
            model="claude-3-opus-20240229",  # Use Claude 3 Opus (latest available model)
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text.strip()
    
    except Exception as e:
        print(f"Error generating Claude LLM response: {e}")
        return "I apologize, but I encountered an error processing your question. Please try again."

