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

selector = [
    {
        "1",
        "日本語のスペシャルエージェント。"
    },
    {
        "2",
        "英語のスペシャルエージェント"
    },
    {
        "3",
        "ドイツ語のスペシャルエージェント"
    },
    {
        "4",
        "断るプロ"
    }
]

prompt = PromptTemplate.from_template(
    '''
    ユーザーからの入力に応じて適切なエージェントを選択して。
    エージェントに付された番号のみ返答して。
    1~3への関連度が低い場合は4を返しなさい。

    ユーザー：{input}
    エージェント：{selector}
    '''
)

chain = prompt | model | StrOutputParser()
result = chain.invoke({"input": "中国の観光名所を教えて", "selector": selector})
print(result)