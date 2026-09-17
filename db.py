import sqlite3
from pathlib import Path

DB_PATH=Path("metadata.db")

def init_db(db_path:Path=DB_PATH):
  conn=sqlite3.connect(db_path)
  cursor=conn.cursor()

  cursor.execute('''CREATE TABLE IF NOT EXISTS documents (id INTEGER PRIMARY KEY AUTOINCREMENT , path TEXT UNIQUE,title  TEXT , author TEXT word_count INT , created_at TIMESTAMP);''')

  cursor.execute("""
  CREATE TABLE IF NOT EXISTS document_tags (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        doc_id INT REFERENCES documents(id),
        tag_name TEXT
    );""")

  conn.commit()
  return conn

def health_check(db_path:Path=DB_PATH)->bool:
  conn=init_db(db_path)
  cursor=conn.cursor()
  cursor.execute("SELECT 1;")
  result=cursor.fetchone()
  conn.close()
  return result==(1,)

if __name__=="__main__":
  if health_check():
    print("DB HEALTH OK")
  else:
    print("DB HELTH NOtOK")
    #db