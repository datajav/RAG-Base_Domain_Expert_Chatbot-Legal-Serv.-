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
            max_chunk_size=max_chunk_size,
            min_chunk_size=min_chunk_size,
            overlap_sentences=overlap_sentences,
            start_chunk_index=chunk_index,
        )
        all_chunks.extend(page_chunks)
        chunk_index += len(page_chunks)
        return all_chunks
    
def chunk_page(
    page_text: str, 
    source: str, 
    page_number: int, 
    max_chunk_size: int, 
    min_chunk_size: int, 
    overlap_sentences: int, 
    start_chunk_index: int, 
) -> list[dict[str, any]]:
    """
    Chunk a single page of text into clause-aware chunks.

    This function uses regex patterns to identify potential clause boundaries
    (like numbered sections or ALL-CAPS headings) and splits the text accordingly.
    It also ensures that chunks are within the specified size limits and includes
    sentence-level overlap for better context.

    Args:
        page_text:         The raw text of the page to be chunked.
        source:            The source identifier (e.g., filename) for metadata.
        page_number:       The original page number from the document.
        max_chunk_size:    Maximum characters per chunk.
        min_chunk_size:    Minimum characters for a valid chunk.
        overlap_sentences: Number of sentences to repeat between chunks.
        start_chunk_index: The starting index for chunk numbering.

    Returns:
        A list of chunk dicts with metadata (see module docstring for schema).
    """
    
    # Implementation goes here, including regex-based splitting and chunk assembling with overlap. This is a complex function that would require careful handling of text boundaries and metadata assignment.

    sections = _split_into_sections(page_text)

    chunks = [] 
    chunk_index = start_chunk_index
    overlap_buffer =  [] 
    
    for section in sections: 
        section_text = section["text"].strip()
        section_number = section["section_number"]
        section_title = section["section_title"]

        if overlap_buffer: 
            section_text = "\n".join(overlap_buffer) + "\n\n" + section_text

        if len(section_text) <= max_chunk_size: 
            if len(section_text) >= min_chunk_size:
                chunks.append(_make_chunk(
                    text=section_text,
                    source=source, 
                    page_number=page_number,
                    chunk_index=chunk_index,
                    section_number=section_number,
                    section_title=section_title,
                       ))
                chunk_index += 1
                overlap_buffer = get_last_sentences(section_text, overlap_sentences)
            else:
                sub_chunks = _split_long_section(
                    text=section_text,
                    max_chunk_size=max_chunk_size,
                    min_chunk_size=min_chunk_size,
                )
            
                for sub_text in sub_chunks:
                    chunks.append(_make_chunk(
                        text=sub_text,
                        source=source, 
                        page_number=page_number,
                        chunk_index=chunk_index,
                        section_number=section_number,
                        section_title=section_title,
                    ))
                    chunk_index += 1
                    overlap_buffer = get_last_n_sentences(sub_chunks[-1], overlap_sentences)

                    return chunks
                

def _split_into_sections(text: str) -> list[dict[str, any]]:
    """
    Use regex patterns to split text into sections based on common legal document structures.

    Returns a list of dicts with keys: section_number, section_title, text.
    """
    # Implementation would involve applying the SECTION_PATTERNS to the text and extracting matches to define section boundaries. Each section would be stored with its number, title, and text content for further processing in chunking.
    pass

section_starts = []

for pattern in SECTION_PATTERNS:
    for match in pattern.finditer(text):
        section_starts.append({
            "pos":match.start(),
            "section_number": _extract_section_number(match), 
            "section_title": _extract_section_title(match)
        })

