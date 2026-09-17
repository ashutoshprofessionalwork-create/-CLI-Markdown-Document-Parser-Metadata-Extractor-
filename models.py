"""blueprint - document table needs : title author word_count and crated_at

a document also has tags (a list of words like ["python","notes"])
"""

from datetime import datetime
from pydantic import BaseModel


class DocumentSchema(BaseModel):
    title: str
    author: str
    word_count: int
    created_at: datetime
    tags: list[str] = []
