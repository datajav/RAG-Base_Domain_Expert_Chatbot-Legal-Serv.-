import chromadb 
from chromadb.utils import embedding_functions
from rich.console import Console 
from rich.progress import track

import os
from pathlib import Path
from typing import Any

Console = Console()

#Constants for Application

COLLECTION_NAME = 
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
    embedding_functions=openai_ef
    metadata={"hnsw:space": "cosine"}
)

return collection


