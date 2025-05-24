from database import get_db_connection
import os
import json
from vectorstore import build_vectorstore

FAISS_META_PATH = "/home/ys0660/25-1/Demo/RAG/faiss_index_ko_sbert/meta.json"

# FAISS로 저장된 항목 수
def get_saved_count():
    if not os.path.exists(FAISS_META_PATH):
        return None
    with open(FAISS_META_PATH, "r") as f:
        meta = json.load(f)
    return meta.get("festival_count")

# FAISS 갱신 후 count수도 갱신
def save_count(count: int):
    os.makedirs(os.path.dirname(FAISS_META_PATH), exist_ok=True)
    with open(FAISS_META_PATH, "w") as f:
        json.dump({"festival_count": count}, f)

# DB에 있는 항목 수
def get_db_count():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM festivals")
    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    return count

# 체크 후 FAISS 갱신 call
def update_vectorstore():
    db_count = get_db_count()
    saved_count = get_saved_count()
    
    if saved_count != db_count:
        print(f"업데이트 필요: saved={saved_count} -> db={db_count}")
        build_vectorstore()
        save_count(db_count)
        print("벡터스토어 재빌드 완료")
    else:
        print("업데이트 불필요, 기존 벡터스토어 사용")
