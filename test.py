import requests
from datetime import datetime

url = "http://202.30.23.34:8000/query"

while True:
    user_input = input("질문을 입력하세요 (종료: exit): ")
    if user_input.lower() == "exit":
        print("프로그램을 종료합니다.")
        break

    # POST 요청 보내기
    response = requests.post(url, json={"user_input": user_input})
    
    # 결과 출력
    print("Status Code:", response.status_code)
    print("Response JSON:", response.json())
