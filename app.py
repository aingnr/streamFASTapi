import streamlit as st
from streamlit_chat import message
from dotenv import load_dotenv
import os

from langchain_openai import ChatOpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)

# Load the OpenAI API key from the environment variable
load_dotenv()

# test that the API key exists
if os.getenv("OPENAI_API_KEY") is None or os.getenv("OPENAI_API_KEY") == "":
    print("OPENAI_API_KEY is not set")
    exit(1)
else:
    print("OPENAI_API_KEY is set")

# setup streamlit page
st.set_page_config(
    page_title="chat.nayaksa",
    page_icon="🤖"
)

def main():
    chat = ChatOpenAI(temperature=0)

    # initialize message history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content="You are a helpful assistant.")
        ]

    st.header("chat.나의약사 🤖")

    # Display message history
    messages = st.session_state.get('messages', [])
    for i, msg in enumerate(messages):
        if isinstance(msg, HumanMessage):
            message(msg.content, is_user=True)
        else:
            message(msg.content, is_user=False)

    # User input at the bottom
    user_input = st.text_input("Your message:", key="user_input")
    send_button = st.button("Send")

    # handle user input
    if send_button and user_input:
        st.session_state.messages.append(HumanMessage(content=user_input))
        with st.spinner("Thinking..."):
            # response = chat(st.session_state.messages)
            response = chat.invoke(messages)
        st.session_state.messages.append(AIMessage(content=response.content))
        # 입력 필드를 비우는 대신 사용자 입력을 처리한 후 페이지를 새로 고침
        # st.session_state.user_input = ""  # 이 줄을 제거
        st.rerun()  # 페이지를 새로 고침하여 입력 필드를 초기화

if __name__ == '__main__':
    main()
