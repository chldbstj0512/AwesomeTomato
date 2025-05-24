from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from database import load_festival_data
import os

# FAISS 인덱스 저장 경로
FAISS_INDEX_PATH = "/home/ys0660/25-1/Demo/RAG/faiss_index_ko_sbert"
LOCAL_MODEL_PATH = "/home/ys0660/25-1/Demo/model/jhgan-ko-sbert"  # 로컬에 복사해놓은 경로

# 벡터스토어 빌드 함수
def build_vectorstore():   
    docs = load_festival_data()
    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = splitter.split_documents(docs)
    embeddings = HuggingFaceEmbeddings(model_name=LOCAL_MODEL_PATH) 
    vectorstore = FAISS.from_documents(texts, embeddings)
    vectorstore.save_local(FAISS_INDEX_PATH)

# 벡터스토어 로드 함수
def load_vectorstore():
    if not os.path.exists(FAISS_INDEX_PATH):
        raise FileNotFoundError(f"FAISS 인덱스 경로가 존재하지 않음: {FAISS_INDEX_PATH}")
    embeddings = HuggingFaceEmbeddings(model_name=LOCAL_MODEL_PATH) 
    return FAISS.load_local(FAISS_INDEX_PATH, embeddings, allow_dangerous_deserialization=True)
