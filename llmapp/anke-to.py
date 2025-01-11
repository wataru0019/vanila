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
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = os.environ.get("LANGSMITH_API_KEY")
os.environ["LANGCHAIN_PROJECT"] = os.environ.get("LANGCHAIN_PROJECT")
os.environ["TAVIRY_API_KEY"] = os.environ.get("TAVIRY_API_KEY")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
model = ChatGoogleGenerativeAI(api_key=GEMINI_API_KEY, model="gemini-1.5-flash")

client = Client()

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "ユーザーの要件に基づき、適切なアンケートを作成しなさい。"),
        ("user", '''
yaml
title: バスツアーアンケート要件定義書

1. 背景:
  description: バスツアーに参加いただいたお客様から、ツアーに関するフィードバックを収集し、今後のツアー改善に役立てるため。

2. 目的:
  description: ツアーの満足度を把握し、特に面白かった点とつまらなかった点を具体的に分析する。  改善すべき点と、強みを明確にすることで、次回以降のツアーの質向上を目指す。

3. 対象者:
  description:  今回のバスツアーに参加された全てのお客様。

4. アンケート実施方法:
  method: オンラインアンケート(例: Googleフォーム、SurveyMonkeyなど)を検討。紙媒体での実施も検討可能。ヒアリングが必要。
  considerations:
    - オンラインアンケートの場合、URLの配布方法(メール、ツアーパンフレットへの記載など)を検討する必要がある。
    - 紙媒体の場合、回収方法、集計方法を検討する必要がある。
    - 回答期限を設定する必要がある。

5. アンケート項目:

  必須項目:
    - 参加者ID(匿名回答の場合は不要。匿名の場合、統計処理のみ行うことを明記する必要がある):  回答者の識別番号(任意)
    - ツアー名: どのツアーに関するアンケートか明確にするため
    - 参加日: どの日のツアーに関するフィードバックか明確にするため

  自由記述項目:
    - ツアーで最も良かった点 (具体的に記述してください):  自由回答で、楽しかった点、良かった点を詳細に記述してもらう。
    - ツアーで最も悪かった点 (具体的に記述してください): 自由回答で、不満だった点、改善すべき点を詳細に記述してもらう。

  選択肢式項目 (ヒアリングにより項目追加・修正が必要):
    - 全体的な満足度:  (非常に満足、満足、普通、不満、非常に不満) 5段階評価
    - ガイドの対応: (非常に良かった、良かった、普通、悪かった、非常に悪かった) 5段階評価
    - バス車両の快適性: (非常に快適、快適、普通、不快、非常に不快) 5段階評価
    - 昼食/夕食の満足度: (非常に満足、満足、普通、不満、非常に不満) 5段階評価
    - 観光地の魅力: (非常に魅力的、魅力的、普通、魅力的でない、全く魅力的でない) 5段階評価
    - ツアーの行程: (非常に良かった、良かった、普通、悪かった、非常に悪かった) 5段階評価
    - その他、改善してほしい点: (自由記述)


6. ヒアリング事項:
  - アンケート実施方法(オンライン/紙媒体、配布方法、回収方法)
  - 回答期限
  - 回答者の属性(年齢層、性別など)に関する質問項目の必要性とその方法(任意回答、匿名回答の場合の統計処理方法)
  - 選択肢式項目の選択肢内容の妥当性と網羅性(上記の項目以外にも必要な項目がないか確認)
  - 回答へのインセンティブの有無 (例: 抽選で景品をプレゼント)
  - 集計方法と分析方法


7. 納期:
  description:  ヒアリング後、1週間以内を目標とする。


8. その他:
  description:  回答データのプライバシー保護について適切な措置を講じる。
        ''')
    ]
)

chain = prompt | model | StrOutputParser()
print(chain.invoke({}))