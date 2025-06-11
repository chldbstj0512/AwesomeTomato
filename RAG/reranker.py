from langchain_core.documents import Document
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from typing import List

class RelevanceScore(BaseModel):
    relevance_score: float = Field(description="문서가 쿼리와 얼마나 관련이 있는지를 나타내는 점수.")

def reranking_documents(query: str, docs: List[Document], top_n: int = 2) -> List[Document]:
    parser = JsonOutputParser(pydantic_object=RelevanceScore)
    prompt = PromptTemplate(
        template="""
        다음 요구에서 찾고자 하는 키워드가 무엇입니까? 장소는 어디입니까?
        키워드와 장소를 고려해 점수를 1~10까지 매기십시오.
        {format_instructions}
        
        question: {query}
        document: {doc}
        relevance_score:
        """,
        input_variables=["query", "doc"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    llm = ChatOpenAI(temperature=0, model="gpt-4o", max_tokens=3000)
    chain = prompt | llm | parser

    scored_docs = []
    for doc in docs:
        try:
            score = float(chain.invoke({"query": query, "doc": doc.page_content})['relevance_score'])
        except Exception as e:
            print(f"오류 발생: {str(e)} → 기본 점수 5점 적용")
            score = 5.0
        scored_docs.append((doc, score))

    reranked = sorted(scored_docs, key=lambda x: x[1], reverse=True)
    return [doc for doc, _ in reranked[:top_n]]
