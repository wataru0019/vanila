from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

# OpenAIのAPIキーを設定
import os
os.environ["OPENAI_API_KEY"] = ""  # ユーザーにAPIキーを設定してもらいます

# LLMの初期化
llm = ChatOpenAI(temperature=0.0)

# メモリの初期化
memory = ConversationBufferMemory()

# 会話チェーンの初期化
conversation = ConversationChain(
    llm=llm,
    memory=memory
)

# チャットボットとの対話
while True:
    user_input = input("あなた: ")
    if user_input.lower() == "終了":
        break
    response = conversation.predict(input=user_input)
    print(f"ボット: {response}")
