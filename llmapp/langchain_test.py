import os
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
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

def test_put(input: str):
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "あなたは優秀な英語教師です。ユーザーから入力された英語を日本語で問題点を指摘してください"),
            ("user", "{input}")
        ]
    )

    chain = prompt | model | StrOutputParser()
    return chain.invoke({"input": input})

print(test_put("Hello, my name is wataru! Nice to meet you!"))