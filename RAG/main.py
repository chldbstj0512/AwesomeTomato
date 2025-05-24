from models import QueryRequest
from rag import run_query
from updatecheck import update_vectorstore
from contextlib import asynccontextmanager
from fastapi import FastAPI
from dotenv import load_dotenv

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. API key 로드
    load_dotenv()
    # 2. PostgreSQL 변화 감지 후 벡터스토어 업데이트
    update_vectorstore()
    yield

# lifespan 연결
app = FastAPI(lifespan=lifespan)

@app.post("/query")
def ask_rag(req: QueryRequest):
    answer = run_query(req.user_input)
    return {"prompt": req.user_input, "answer": answer}
