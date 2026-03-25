import re 
from typing import Any

SECTION_PATTERNS = [

    re.compile(r"^(\d+\.(?:d+\.?)*)\s+([A-Z][^\n]{0,80}})", re.multiline), 

    re.compile(r"^(Article|Section|ARTICLE|SECTION)\s+(\d+\.?\d*\.?\d*)\s*[:\--]?\s*([A-Z][^\n]{0,80})?", re.MULTILINE), 

    
    
]