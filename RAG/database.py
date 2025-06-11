import psycopg2
from langchain_core.documents import Document

def get_db_connection():
    return psycopg2.connect(
        dbname="ragdb",
        user="postgres",
        password="1234",
        host="localhost",
        port="5432"
    )

def load_festival_data():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT name, location, start_date, end_date, description, contents, homepage
        FROM festivals""")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    documents = []
    for row in rows:
        text = (
            f"{row[0]}{row[4]}{row[5]}"  # description + contents 같은 본문 텍스트만 담음
        )
        metadata = {
            "name": row[0],
            "location": row[1],
            "start_date": str(row[2]),
            "end_date": str(row[3]),
            "homepage": row[6]
        }
        documents.append(Document(page_content=text, metadata=metadata))
    return documents

load_festival_data()