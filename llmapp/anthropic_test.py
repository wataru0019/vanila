import os
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from langchain_anthropic import ChatAnthropic
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

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
model = ChatAnthropic(api_key=ANTHROPIC_API_KEY, model="claude-3-haiku-20240307")

client = Client()

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
    prompt = ChatPromptTemplate.from_messages([
        ("user", f"{state.color}の内容が「赤色」を指している場合はTrueをそうでない場合が、Falseと回答しなさい。データタイプはpythonのbool型とすること")
    ])
    chain = prompt | llm
    result = chain.invoke({})
    print(result.judge)
    state.judge = result.judge
    return state
    
def root_node(state: State) -> bool:
    print(f"途中経過{state}")
    return state.judge

def true_node(state: State):
    print("true")
    return state

def false_node(state: State):
    print("false")
    return state

workflow = StateGraph(State)

workflow.add_node("choice_color_node", choice_color)
workflow.add_node("conditional_node", conditional_node)
workflow.add_node("root_node", root_node)
workflow.add_node("true_node", true_node)
workflow.add_node("false_node", false_node)

workflow.add_edge(START, "choice_color_node")
workflow.add_edge("choice_color_node", "conditional_node")
workflow.add_conditional_edges(
    "conditional_node",
    root_node,
    {True: "true_node", False: "false_node"}
)

chain = workflow.compile()
chain.invoke({"input": "トマト", "color": "", "judge": False})