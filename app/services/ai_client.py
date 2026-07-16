import requests

def get_embedding(text: str) -> list[float]:
    """
    Calls the local Ollama container to generate an embedding for a string.
    """
    response = requests.post(
        "http://ollama:11434/api/embeddings",
        json={"model": "nomic-embed-text", "prompt": text}
    )
    if response.status_code != 200:
        raise Exception("Failed to generate embedding from Ollama")
    return response.json()["embedding"]