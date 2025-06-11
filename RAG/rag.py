from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage
from vectorstore import load_vectorstore
from reranker import reranking_documents
from langchain_community.chat_message_histories import ChatMessageHistory
from dotenv import load_dotenv

from datetime import datetime

load_dotenv()

def init_chat_history():
    return ChatMessageHistory()

# 한 턴 실행 함수
def run_query(user_input: str, chat_history: ChatMessageHistory) -> str:
    vectorstore = load_vectorstore()
    retriever = vectorstore.as_retriever(search_kwargs={"k": 30})

    today = datetime.now().strftime("%Y년 %m월 %d일")
    dated_input = f"오늘은 {today}이야. {user_input}"

    initial_docs = retriever.get_relevant_documents(dated_input)

    # reranked_docs = reranking_documents(user_input, initial_docs, top_n=2)
    # context = "\n\n---\n\n".join([doc.page_content for doc in reranked_docs])
    
    context = "\n\n---\n\n".join([doc.page_content for doc in initial_docs])

    print(context)

    today = datetime.now().strftime("%Y년 %m월 %d일")  # 예: "2025년 05월 23일"
    prompt = f"""
    [시스템 프롬프트]
    당신은 대한민국의 축제 정보에 대해 잘 알고 있는 AI이에요.  
    사용자가 사는 지역, 현재 날짜와 시기를 바탕으로 갈만한 축제를 따뜻하고 친근한 말투로 추천해주세요.  
    만약 추천하고 싶은 행사의 날짜가 2025년 이전이라면, 25년 00월 개최 예정 이라고 알려주세요.
    추천 시에는 축제 이름, 위치, 날짜, 특징을 간략하게 요약해주세요.  
    오늘은 {today}이에요. 되도록 오늘과 가까운 시기의 행사를 추천하세요.
    
    문서:
    {context}

    질문:
    {user_input}
    
    답변:
    """.strip()

    # 사용자 입력 저장
    chat_history.add_user_message(user_input)

    # LLM 초기화
    llm = ChatOpenAI(model="gpt-4o", temperature=0)

    # 기존 대화 이력 + 현재 프롬프트를 모두 전달
    messages = chat_history.messages + [HumanMessage(content=prompt)]
    response = llm(messages)

    # 응답 저장
    chat_history.add_ai_message(response.content)

    return response.content
