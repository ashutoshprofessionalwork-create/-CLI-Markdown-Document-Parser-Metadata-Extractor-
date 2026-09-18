"""CLI Markdown Document Parser & Metadata Extractor
A beginner-friendly project to build confidence in command-line tooling and structured data persistence. Create a Python CLI tool that parses markdown files, extracts YAML frontmatter, validates metadata schemas with Pydantic, and indexes document headings and tags into a local SQLite database."""

"""pip install typer python-frontmatter pydantic rich"""

import re
from pathlib import Path
from datetime import datetime
import yaml
from models import DocumentSchema
import time

class MarkdownParser:
    def __init__ (self,path:Path):
        self.path=Path(path)

    def parse_md(self)->DocumentSchema:
        start_time=time.perf_counter() # start timer
        raw_text=self.path.read_text(encoding="utf-8")

        pattern = r"^---\s*\n(.*?)\n---\s*\n(.*)$"
        match=re.search(pattern,raw_text,re.DOTALL)
        
        #REPLACING THIS TO HANDLE EDGE CASES
        
        # if not match:
        #     raise ValueError(f"No YAML frontmatter found in {self.path}")
        # frontmatter_raw,body=match.groups()
        # data=yaml.safe_load(frontmatter_raw) or {}

        if match:
            frontmatter_raw,body=match.groups()
            try:
                data=yaml.safe_load(frontmatter_raw) or {}
            except yaml.YAMLError:
                data={}
        else:
            data={}
            body=raw_text
        
        # Calculate word count from the body text
        words = body.split()
        word_count = len(words)
        
        #stop timer -> calculate time
        elapsed_ms=(time.perf_counter()- start_time)*1000
        print(f"parsed {self.path.name} in {elapsed_ms:.2f} ms")

        # validate with pydantic model
        return DocumentSchema(
            title=data.get("title", self.path.stem),
            author=data.get("author", "Unknown"),
            word_count=word_count,
            created_at=data.get("created_at", datetime.now()),
            tags=data.get("tags", []),
        )
        
    def chunk_content(self,max_words_per_chunk: int = 150 ) -> list[str]:
        raw_text=self.path.read_text(encoding="utf-8")
        #strip frontmatter if present so we only chunk actual body text
        pattern = r"^---\s*\n(.*?)\n---\s*\n(.*)$"
        match = re.search(pattern, raw_text, re.DOTALL)
        #same thing -> body = match.group(2).strip() if match else raw_text.strip()
        if match:
            body=match.group(2).strip()
        else:
            body=raw_text.strip()
        
        #splits along md para breaks
        
        paragraphs=[]
        for p in body.split("\n\n"):
            p=p.strip()
            
            if p:
                paragraphs.append(p)
        
        chunks=[]
        current_chunk=[]
        current_words=0
        for para in paragraphs:
            #total number of work in 1 line -> "-----"
            para_word_count=len(para.split())
            
            if (current_words + para_word_count>max_words_per_chunk and current_chunk):
                chunks.append("\n\n".join(current_chunk))
                current_chunk=[para]
                current_words =para_word_count
                
            else:
                current_chunk.append(para)
                current_words+=para_word_count
                
        if current_chunk:
            chunks.append("\n\n".join(current_chunk))
        
        return chunks
            
            

if __name__=="__main__":
    test_file=Path("Sample.md")
    parser=MarkdownParser(test_file)
    doc=parser.parse_md()
    print(f"Title: {doc.title} | Author: {doc.author} | Words: {doc.word_count}")
    
    #test chunking with a small word limit 
    chunks=parser.chunk_content(max_words_per_chunk=20)
    print(f"\nGenerated{len(chunks)} chunks: ")
    for idx,chunk in enumerate(chunks,1):
        print(f"--Chunk {idx} ({len(chunk.split())} words)---")
        print(chunk)