"""CLI Markdown Document Parser & Metadata Extractor
A beginner-friendly project to build confidence in command-line tooling and structured data persistence. Create a Python CLI tool that parses markdown files, extracts YAML frontmatter, validates metadata schemas with Pydantic, and indexes document headings and tags into a local SQLite database."""

"""pip install typer python-frontmatter pydantic rich"""

import re
from pathlib import Path
from datetime import datetime
import yaml
from mdparser.models import DocumentSchema

class MarkdownaParser:
    def __init__ (self,path:Path):
        self.path=Path(path)

    def parse_md(self)->DocumentSchema:
        raw_text=self.path.read_text(encoding="utf-8")

        pattern = r"^---\s*\n(.*?)\n---\s*\n(.*)$"
        match=re.search(pattern,raw_text,re.DOTALL)

        if not match:
            raise ValueError(f"No YAML frontmatter found in {self.path}")

        frontmatter_raw,body=match.groups()
        data=yaml.safe_load(frontmatter_raw) or {}

        # Calculate word count from the body text
        words = body.split()
        word_count = len(words)

        # Build and validate with our Pydantic model
        return DocumentSchema(
            title=data.get("title", self.path.stem),
            author=data.get("author", "Unknown"),
            word_count=word_count,
            created_at=data.get("created_at", datetime.now()),
            tags=data.get("tags", []),
        )
