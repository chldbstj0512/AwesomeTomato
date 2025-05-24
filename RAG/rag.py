from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from vectorstore import load_vectorstore

def run_query(user_input: str) -> str:
    vs = load_vectorstore()
    retriever = vs.as_retriever(search_kwargs={"k": 5})
    qa = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(model="gpt-4", temperature=0),
        retriever=retriever
    )
    return qa.run(user_input)
