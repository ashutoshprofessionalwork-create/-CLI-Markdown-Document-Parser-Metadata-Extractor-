import sqlite3
from pathlib import Path

DB_PATH = Path("metadata.db")


def init_db(db_path: Path = DB_PATH):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(
    """CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT , 
        path TEXT UNIQUE,
        title  TEXT , 
        author TEXT ,
        word_count INT , 
        created_at TIMESTAMP
    );"""
    )

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS document_tags (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        doc_id INT REFERENCES documents(id) ON DELETE CASCADE,
        tag_name TEXT
    );""")
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_tag_name ON document_tags(tag_name);
        """)

    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_path ON documents(path)
        ''')
    
    conn.commit()
    return conn

#select 1 bw -- content --
def health_check(db_path: Path = DB_PATH) -> bool:
    conn = init_db(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT 1;")
    result = cursor.fetchone()
    conn.close()
    return result == (1,)

def seed_data(db_path:Path=DB_PATH):
    conn=init_db(db_path)
    cursor=conn.cursor()
    
    cursor.execute('DELETE  FROM document_tags;')
    cursor.execute('DELETE  FROM documents;')
    
    #mock data
    #syntax-->path,title,author,word_count,created_at,tags
    mock_docs = [
        ("docs/intro.md", "Introduction to Python", "Ash", 250, "2026-09-18 10:00:00", ["python", "beginners"]),
        ("docs/advanced.md", "Async Architectures", "Alex", 1200, "2026-09-18 11:30:00", ["python", "backend"]),
        ("docs/docker.md", "Container Basics", "Jordan", 600, "2026-09-18 12:00:00", ["devops", "docker"])
    ]
    
    for path,title,author,word_count,created_at,tags in mock_docs:
        cursor.execute("""
        INSERT INTO documents (path,title,author,word_count,created_at)      
        VALUES(?,?,?,?,?);         
        """,(path,title,author,word_count,created_at))
        
        doc_id=cursor.lastrowid
        for tag in tags:
            cursor.execute("""
            INSERT INTO document_tags (doc_id,tag_name)
            VALUES(?,?);               
            """,(doc_id,tag))
    conn.commit()
    conn.close()
    print("DB SEEDED with mock data -> succus")


if __name__ == "__main__":
    seed_data()
    # if health_check():
    #     print("DB HEALTH OK")
    # else:
    #     print("DB HELTH NOtOK")
    #     # db


