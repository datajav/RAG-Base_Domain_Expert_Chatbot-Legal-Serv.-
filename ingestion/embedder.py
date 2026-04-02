import chromadb 
from chromadb.utils import embedding_functions
from rich.console import Console 
from rich.progress import track

import os
from pathlib import Path
from typing import Any

Console = Console()

#Constants for Application

COLLECTION_NAME = "LegalMind RAG"
CHROMA_PERSIST_DIR = "./chroma_db" 
EMBEDDING_MODEL = "text-embedding-3-small"

def get_chroma_client() -> chromadb.PersistentClient: 

    return chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)

def get_collection(client: chromadb.PersistentClient) -> chromadb.Collection:

    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
        api_key=os.getenv("OPENAI_API_KEY"), 
        model_name=EMBEDDING_MODEL
    )

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=openai_ef,
        metadata={"hnsw:space": "cosine"}
    )

    return collection


#Ingestion Helpers

def embed_and_store(chunks: list[dict[str, Any]], reset: bool = False) -> chromadb.Collection:
    client = get_chroma_client()

    if reset:
        Console.print("[yellow] Resetting collection - deleting existing vectors...[/yellow]")
        try:
            client.delete_collection(COLLECTION_NAME)
        except Exception:
            pass

    collection = get_collection(client)
    existing_count = collection.count()

    if existing_count > 0:
        Console.print(f"\n[bold yellow] Embedding {len(chunks)} chunks into ChromaDB collection '{COLLECTION_NAME}' (existing vectors: {existing_count})...[/bold yellow]")
        Console.print(f" Model: {EMBEDDING_MODEL}")
        Console.print(f" Storage: {CHROMA_PERSIST_DIR}\n")



