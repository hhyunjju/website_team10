from django.shortcuts import render
import threading
import gradio as gr
from django.http import HttpResponse
# -----------
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.document_loaders import CSVLoader
import dotenv
dotenv.load_dotenv()
import time

persist_directory = './'
embedding = OpenAIEmbeddings()

# load from disk
vectorstore = Chroma(
    persist_directory=persist_directory,
    embedding_function=embedding)

retriever = vectorstore.as_retriever()

from langchain.agents.agent_toolkits import create_retriever_tool

tool = create_retriever_tool(
    retriever,
    "BarunJaseDowoomi_customer_service_guide",
    "Searches and returns information regarding the customer service guide.",
)
tools = [tool]

from langchain.chat_models import ChatOpenAI
llm = ChatOpenAI(temperature=0, model='gpt-3.5-turbo-1106')

# This is needed for both the memory and the prompt
memory_key = "history"

from langchain.agents.openai_functions_agent.agent_token_buffer_memory import (
    AgentTokenBufferMemory,
)

memory = AgentTokenBufferMemory(memory_key=memory_key, llm=llm)

from langchain.agents.openai_functions_agent.base import OpenAIFunctionsAgent
from langchain.schema.messages import SystemMessage
from langchain.prompts import MessagesPlaceholder

system_message = SystemMessage(
    content=(
        "You are a customer service agent for '바른자세 도우미'. "
        "Do your best to answer the questions within the scope of our service. "
        "Please do not provide answers that deviate from the subject matter. "
        "Feel free to use any tools available to look up "
        "relevant information, only if necessary"
        "If you don't know the answer, just say you don't know. Don't try to make up an answer."
        "Make sure to answer in Korean"
    )
)

prompt = OpenAIFunctionsAgent.create_prompt(
    system_message=system_message,
    extra_prompt_messages=[MessagesPlaceholder(variable_name=memory_key)],
)

agent = OpenAIFunctionsAgent(llm=llm, tools=tools, prompt=prompt)

from langchain.agents import AgentExecutor

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True,
    return_intermediate_steps=True,
)

# result = agent_executor({"input": "사용요금 조회는 어떻게 하죠"})
# result["output"]

# ---------------- ~ langchain model 만들기 -------------
# LangChain 라이브러리에서 필요한 컴포넌트 가져오기
from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage

# GPT-3.5 모델과 히스토리를 기반으로 답변 생성하는 함수 정의
def response(message, history, additional_input_info):
    history_langchain_format = []
    for human, ai in history:
        history_langchain_format.append(HumanMessage(content=human))
        history_langchain_format.append(AIMessage(content=ai))
    # 새로운 사용자 메시지 추가
    history_langchain_format.append(HumanMessage(content=message))
    
    # AgentExecutor를 사용하여 응답 생성
    result = agent_executor({"input": message, "history": history_langchain_format})
    
    # LangChain의 출력에서 AI의 마지막 메시지 가져오기
    ai_response = result['output']
    return ai_response

# Gradio 챗봇 인터페이스 구성 및 실행
# gr.ChatInterface(
#     fn=response,
#     textbox=gr.Textbox(placeholder="여기에 메시지를 입력하세요...", container=False, scale=7),
#     chatbot=gr.Chatbot(height=1000),  # 채팅창의 높이 조절
#     title="바른자세 도우미 챗봇",
#     description="고객 서비스 관련 질문에 답변합니다. 질문을 입력해주세요.",
#     theme="monochrome",  # 인터페이스 테마 설정
#     examples=[["안녕하세요"], ["배송 상태를 알고 싶어요"]],
#     retry_btn="다시 입력 ↩",
#     undo_btn="이전 메시지 삭제 ❌",
#     clear_btn="채팅 기록 삭제 💫",
#     additional_inputs=[
#         gr.Textbox("", label="추가 입력 정보", placeholder="여기에 추가 정보를 입력하세요.")
#     ]
# ).launch(share=True)

def launch_gradio():
    gr.Interface(
        fn=response,
        textbox=gr.Textbox(placeholder="여기에 메시지를 입력하세요...", container=False, scale=7),
        chatbot=gr.Chatbot(height=500),  # 채팅창의 높이 조절
        description="고객 서비스 관련 질문에 답변합니다. 질문을 입력해주세요.",
        theme="monochrome",  # 인터페이스 테마 설정
        examples=[["안녕하세요"], ["배송 상태를 알고 싶어요"]],
        retry_btn="다시 입력 ↩",
        undo_btn="이전 메시지 삭제 ❌",
        clear_btn="채팅 기록 삭제 💫",
        additional_inputs=[
            gr.Textbox("", label="추가 입력 정보", placeholder="여기에 추가 정보를 입력하세요.")
        ]
    ).launch(share=True, server_name="127.0.0.1", server_port=7860)
# gradio 인터페이스 실행
threading.Thread(target=launch_gradio, daemon=True).start()

def chatbot_view(request):
    return render(request, 'chatbot/chatbot.html')

