import os
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from langgraph.graph import StateGraph, START
from pydantic import BaseModel, Field
from typing import TypedDict
from langsmith import Client
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from google.oauth2 import service_account
import vertexai
from vertexai.generative_models import GenerativeModel, Part
from langchain_google_vertexai import ChatVertexAI

load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = os.environ.get("LANGSMITH_API_KEY")
os.environ["LANGCHAIN_PROJECT"] = os.environ.get("LANGCHAIN_PROJECT")
os.environ["TAVIRY_API_KEY"] = os.environ.get("TAVIRY_API_KEY")

SERVICE_ACCOUNT_FILE = 'venv/gemini-code-assistant-439214-86628f3e83a9.json'
PROJECT_ID = "gemini-code-assistant-439214"
LOCATION = "us-central1"

creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE
)
vertexai.init(project=PROJECT_ID, location=LOCATION, credentials=creds)

model = ChatVertexAI(model="gemini-1.5-flash-002", credentials=creds)

class State(BaseModel):
    input: str = Field(description="ユーザー入力")
    color: str = Field(description="果物の色")
    judge: bool = Field(description="青色か否か")

llm = model.with_structured_output(State)

def choice_color(state: State) -> State:
    prompt = PromptTemplate.from_template('''
    ユーザーから入力された果物の色を回答してください。

    ユーザー：{input}
    ''')
    chain = prompt | llm
    result = chain.invoke({"input": state.input})
    state.color = result.color
    return state

def conditional_node(state: State) -> State:
    prompt = PromptTemplate.from_template(
        "{color}の内容が「赤色」を指している場合はTrueをそうでない場合が、Falseと回答しなさい。データタイプはpythonのbool型とすること"
    )
    chain = prompt | llm
    result = chain.invoke({"color": state.color})
    print(result.judge)
    return state

workflow = StateGraph(State)

workflow.add_edge(START, "choice_color")
workflow.add_sequence([choice_color, conditional_node])

chain = workflow.compile()
chain.invoke({"input": "バナナ", "color": "", "judge": False})