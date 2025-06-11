import gradio as gr
import requests

SERVER_URL = "http://localhost:8000/query"

def respond(message, chat_history):
    chat_history.append((message, "💬 답변을 준비 중이에요..."))
    # print("📝 [현재 chat history]", chat_history)  # 디버깅용 출력

    yield "", chat_history

    try:
        response = requests.post(SERVER_URL, json={"user_input": message})
        if response.status_code == 200:
            answer = response.json()["answer"]
        else:
            answer = "⚠️ 서버 오류가 발생했어요."
    except Exception:
        answer = "⚠️ 서버 연결에 실패했어요."

    chat_history[-1] = (message, answer)
    yield "", chat_history

def reset_chat():
    return "", []

# Gradio UI 구성
with gr.Blocks(theme=gr.themes.Soft(), css=".gr-chatbot { height: 500px; }") as demo:
    gr.Markdown(
        """
        # 🍅 지역 축제 추천 챗봇
        지역 기반으로 요즘 떠오르는 축제를 추천해드릴게요!</br>
        **예시:** `이번 주말에 갈만한 축제 알려줘`, `대구 근처 여름 축제 추천`
        """,
        elem_id="title"
    )

    chatbot = gr.Chatbot(label="축제 챗봇", show_copy_button=True, bubble_full_width=False)
    msg = gr.Textbox(
        label="질문을 입력해주세요.",
        placeholder="예: 다음 주에 가족과 갈만한 축제 있을까요?",
        lines=1,
        autofocus=True
    )
    clear = gr.ClearButton([msg, chatbot])
    clear.click(reset_chat, inputs=None, outputs=[msg, chatbot])

    msg.submit(respond, [msg, chatbot], [msg, chatbot])

if __name__ == "__main__":
    demo.launch()
