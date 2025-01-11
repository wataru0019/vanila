import os
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from langchain_anthropic import ChatAnthropic
from langgraph.graph import StateGraph, START, END
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
    query: str = Field(description="ユーザーからの問い")
    query_deep: str = Field(description="ユーザーからの問いを深堀する")
    statemant: str = Field(description="意見のまとめ。どんどんブラッシュアップされる")
    counter: int = Field(description="意見交換の回数")
    judge: bool = Field(description="まとめた意見の適正度")
    reason: str = Field(description="評価理由")

class Deeper(BaseModel):
    query_deep: str = Field(description="ユーザーからの問いを深堀する")

class Statement(BaseModel):
    statemant: str = Field(description="意見のまとめ。どんどんブラッシュアップされる")

class Judgement(BaseModel):
    judge: bool = Field(description="まとめた意見の適正度")
    reason: str = Field(description="評価理由")

# llm_state = model.with_structured_output(State)
llm_deeper = model.with_structured_output(Deeper)
llm_statement = model.with_structured_output(Statement)
llm_judge = model.with_structured_output(Judgement)

def deeper(state: State) -> State:
    prompt = PromptTemplate.from_template(f'''
    ユーザーからの問いをAIが議論しやすいよう、社会的意義・人類への影響・日本への影響の３つ観点を深堀できるような問いを生成しなさい。

    ユーザーからの問い：{state.query}
    ''')

    deeper_chain = prompt | llm_deeper
    result = deeper_chain.invoke({"query_deep": ""})
    print(result)
    state.query_deep = result.query_deep
    return state

def giron1(state: State) -> State:
    prompt = PromptTemplate.from_template('''
    問いに対する見解を述べよ。

    問い：{query_deep}
    ''')
    giron1_chain = prompt | llm_statement
    result = giron1_chain.invoke({"query_deep": state.query_deep})
    state.statemant = result.statemant
    return state

def giron2(state: State) -> State:
    prompt = PromptTemplate.from_template('''
    以下のcontextをブラッシュアップし、より洗練された意見を述べよ。

    context：{context}
    ''')
    giron2_chain = prompt | llm_statement
    result = giron2_chain.invoke({"context": state.statemant})
    state.statemant = result.statemant
    state.counter = state.counter + 1
    print(state.statemant)
    return state

def judgement(state: State) -> State:
    prompt = PromptTemplate.from_template('''
    以下のcontextの内容を評価し、80点以上と評価する場合はTrueをそうでない場合Falseを応答せよ。
    なお、評価は厳しく行うこととする。

    context:{context}
    ''')
    judge_chain = prompt | llm_judge
    result = judge_chain.invoke({"context": state.statemant})
    state.judge = result.judge
    state.reason = result.reason
    return state

def rooting(state: State) -> bool:
    if state.judge or state.counter > 5:
        return True
    else:
        return False

workflow = StateGraph(State)

workflow.add_node("deeper_node", deeper)
workflow.add_node("giron1_node", giron1)
workflow.add_node("giron2_node", giron2)
workflow.add_node("judgement_node", judgement)

workflow.add_edge(START, "deeper_node")
workflow.add_edge("deeper_node", "giron1_node")
workflow.add_edge("giron1_node", "giron2_node")
workflow.add_edge("giron2_node", "judgement_node")
workflow.add_conditional_edges(
    "judgement_node",
    rooting,
    {True: END, False: "giron2_node"}
)

chain = workflow.compile()
chain.invoke({"query": "地球温暖化はこれからも進行していくのか", "query_deep": "", "statemant": "", "counter": 0, "judge": False, "reason": ""})