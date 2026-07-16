import requests

def generate_answer(context: str, question: str) -> str:
    """
    Synthesizes an answer using the retrieved context and the user's question.
    """
    prompt = f"""
    You are an expert Compliance Auditor.
    Use the following document context to answer the user's question.
    If the answer is not in the context, say you don't have enough information.
    Always cite the source document.

    Context:
    {context}

    Question:
    {question}
    """
    
    response = requests.post(
        "http://ollama:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )
    return response.json().get("response", "Error generating response.")