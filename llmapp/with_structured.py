import os
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START
from pydantic import BaseModel, Field
from typing import TypedDict
from langsmith import Client
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage

load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = os.environ.get("LANGSMITH_API_KEY")
os.environ["LANGCHAIN_PROJECT"] = os.environ.get("LANGCHAIN_PROJECT")
os.environ["TAVIRY_API_KEY"] = os.environ.get("TAVIRY_API_KEY")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
model = ChatOpenAI(api_key=OPENAI_API_KEY, model="gpt-4o-mini")

client = Client()

class State(TypedDict):
    teams: list[str]
    playlers: list[str]

llm = model.with_structured_output(State, method="json_mode")
# output_parser = PydanticOutputParser(pydantic_object=State)
# format_instructions = output_parser.get_format_instructions()

# prompt = PromptTemplate.from_template('''
# 日本のプロ野球チームと代表的な選手をリスト形式で出力して。結果をjson形式で返してください。
# ''')
# chain = prompt | llm
# print(chain.invoke({}))

def discover_teams(state: State) -> State:
    prompt = PromptTemplate.from_template('''
    日本のプロ野球チームを出力しなさい。結果をjson形式で返しなさい。
    ''')
    chain = prompt | llm
    result = chain.invoke({})
    state["teams"] = result
    print(state["teams"])
    return state

def discover_playlers(state: State) -> State:
    prompt = PromptTemplate.from_template('''
    以下リストのチーム毎に代表選手をあげなさい。結果をjson形式で返しなさい。

    リスト：{teams}
    ''')
    chain = prompt | llm
    result = chain.invoke({"teams": state["teams"]})
    state["players"] = result
    print(state["players"])
    return state

workflow = StateGraph(State)

workflow.add_sequence([discover_teams, discover_playlers])
workflow.add_edge(START, "discover_teams")

chain = workflow.compile()
chain.invoke({"teams": [], "players": []})