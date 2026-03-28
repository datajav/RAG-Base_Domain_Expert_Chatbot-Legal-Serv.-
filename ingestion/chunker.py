import re 
from typing import Any

SECTION_PATTERNS = [

    re.compile(r"^(\d+\.(?:d+\.?)*)\s+([A-Z][^\n]{0,80}})", re.multiline), 

    re.compile(r"^(Article|Section|ARTICLE|SECTION)\s+(\d+\.?\d*\.?\d*)\s*[:\--]?\s*([A-Z][^\n]{0,80})?", re.MULTILINE), 
    # ALL-CAPS headings (common in contracts): "INDEMNIFICATION", "GOVERNING LAW"
    re.compile(r"^([A-Z][A-Z\s]{4,60})$", re.MULTILINE),
    
]


def chunk_legal_document(
    pages: list[dict[str, Any]], 
    max_chunk_size: int = 1200,
    min_chunk_size: int = 100, 
    overlap_sentences: int = 2,
) -> list[dict[str, Any]]:

    """
    Convert a list of raw pages into clause-aware chunks.

    Args:
        pages:              Output from ingestion/loader.py
        max_chunk_size:     Max characters per chunk (larger than generic RAG
                            because legal clauses need more context)
        min_chunk_size:     Ignore chunks shorter than this (usually headers)
        overlap_sentences:  How many sentences to repeat between chunks
                            for continuity (replaces character-based overlap)

    Returns:
        List of chunk dicts (see module docstring for schema)
    """
    
    all_chunks = []
    chunk_index = 0

    for page in pages: 
        page_chunks = chunk_page(
            page_text=page["text"], 
            source=page["text"],
            page_number=page["page_number"], 
            max_chunk_size=max_chunk_size
            min_chunk_size=min_chunk_size
            overlap_sentences=overlap_sentences
            start_chunk_index=chunk_index
        )
        all_chunks.extend(page_chunks)
        chunk_index += len(page_chunks)
        return all_chunks
    