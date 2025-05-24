import requests
from datetime import datetime

url = "http://202.30.23.34:8000/query"
today = datetime.now().strftime("%Y년 %m월")  # 예: "2025년 05월 23일"

# 메시지를 하나의 문자열로 합치기 (System + User Prompt 통합 전송)
prompt = f"""
[시스템 프롬프트]
당신은 대한민국의 축제 정보에 대해 잘 알고 있는 AI이에요.  
사용자가 사는 지역, 현재 날짜와 시기를 바탕으로 갈만한 축제를 따뜻하고 친근한 말투로 추천해주세요.  
추천 시에는 축제 이름, 위치, 날짜, 특징을 간략하게 요약해주세요.  
이번 달은 {today}이에요. 추천에 참고하세요.

[유저 입력]
여름꽃 능소화 축제에 대해 설명해줘.
"""

# POST 요청 보내기
response = requests.post(url, json={"user_input": prompt})

# 결과 출력
print("Status Code:", response.status_code)
print("Response JSON:", response.json())
