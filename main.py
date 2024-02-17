from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os

from langchain_openai import ChatOpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)

load_dotenv()

# OpenAI API 키 확인
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY is None or OPENAI_API_KEY == "":
    raise EnvironmentError("OPENAI_API_KEY가 설정되지 않았습니다.")

app = FastAPI()
chat = ChatOpenAI(temperature=0)

class ChatRequest(BaseModel):
    messages: list[str]

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    messages = [
        SystemMessage(content="You are a helpful assistant.")
    ]
    for msg in request.messages:
        messages.append(HumanMessage(content=msg))
    
    response = chat(messages)
    if not response:
        raise HTTPException(status_code=500, detail="챗봇 응답 실패")

    return {"answer": response.content}