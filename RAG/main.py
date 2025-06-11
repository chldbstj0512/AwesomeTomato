# main.py
from models import QueryRequest
from rag import run_query, init_chat_history
from updatecheck import update_vectorstore
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from dotenv import load_dotenv
from langchain_community.chat_message_histories import ChatMessageHistory

@asynccontextmanager
async def lifespan(app: FastAPI):
    load_dotenv()
    update_vectorstore()
    app.state.chat_history = init_chat_history()

    yield

app = FastAPI(lifespan=lifespan)

@app.post("/query")
def ask_rag(req: QueryRequest, request: Request):
    # ChatMessageHistory를 전역 또는 main 루프에서 관리
    chat_history = request.app.state.chat_history
    answer = run_query(req.user_input, chat_history)
    return {"prompt": req.user_input, "answer": answer}
