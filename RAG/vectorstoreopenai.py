from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from database import load_festival_data
import os
from dotenv import load_dotenv

load_dotenv()

FAISS_INDEX_PATH = "/home/ys0660/25-1/Demo/RAG/openAI"

def build_vectorstore():
    docs = load_festival_data()
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=200)
    texts = splitter.split_documents(docs)
    embeddings = OpenAIEmbeddings() 
    
    # (텍스트, 임베딩) 튜플 생성
    text_embeddings = []
    for doc in texts:
        embedding = embeddings.embed_query(doc.page_content)
        text_embeddings.append((doc.page_content, embedding))

    # FAISS 벡터스토어 생성
    vectorstore = FAISS.from_embeddings(text_embeddings, embedding=embeddings)
    vectorstore.save_local(FAISS_INDEX_PATH)


def load_vectorstore():
    if not os.path.exists(FAISS_INDEX_PATH):
        raise FileNotFoundError(f"FAISS 인덱스 경로가 존재하지 않음: {FAISS_INDEX_PATH}")
    embeddings = OpenAIEmbeddings()
    return FAISS.load_local(FAISS_INDEX_PATH, embeddings, allow_dangerous_deserialization=True)
