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
    query: str
    answer: str
    summary: str

def english_teacher(state: State) -> State:
    prompt = ChatPromptTemplate.from_messages([
        ("system", "あなたは英語教師です。ユーザーから入力された英作文の文法的は問題点を指摘しなさい。"),
        ("user", "{query}")
    ])
    chain = prompt | model | StrOutputParser()
    state["answer"] = chain.invoke({"query": state["query"]})
    return state

def summarizer(state: State) -> State:
    prompt = PromptTemplate.from_template('''
    {context}を踏まえこれからの学習計画を立てなさい。
    ''')
    chain = prompt | model | StrOutputParser()
    state["summary"] = chain.invoke({"context": state["answer"]})
    print(state["summary"])
    return state

workflow = StateGraph(State)

workflow.add_edge(START, "english_teacher")
workflow.add_sequence([english_teacher, summarizer])

chain = workflow.compile()
print(chain.invoke(State({"query": "Hello, My name is Wataru Kashihawa. Im thirty three yeards old. Im from Japan. My Job is sales, but im not good sales lol..."})))