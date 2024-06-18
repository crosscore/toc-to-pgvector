from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv
import os
from pydantic import Field
from typing import List

# カスタムチャットメッセージ履歴クラス
class LimitedChatMessageHistory(ChatMessageHistory):
    max_messages: int = Field(default=10)
    max_characters: int = Field(default=1000)  # 新しい上限設定

    def __init__(self, max_messages=10, max_characters=1000):
        super().__init__()
        self.max_messages = max_messages
        self.max_characters = max_characters

    def add_message(self, message):
        super().add_message(message)
        # メッセージ数の制限
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]
        # 文字数の制限
        total_characters = sum(len(msg.content) for msg in self.messages)
        while total_characters > self.max_characters:
            self.messages.pop(0)
            total_characters = sum(len(msg.content) for msg in self.messages)

load_dotenv()
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")

MAX_MESSAGE = 10
MAX_CHARACTERS = 1000  # 新しい上限設定

llm = AzureChatOpenAI(
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    azure_deployment=AZURE_OPENAI_DEPLOYMENT,
    api_version=AZURE_OPENAI_API_VERSION,
    temperature=0.7,
    max_tokens=256,
    model_kwargs={
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0,
    }
)

# プロンプトテンプレートで会話履歴を追加
prompt_template = ChatPromptTemplate.from_messages(
    [
        MessagesPlaceholder(variable_name="history"),  # 会話履歴の追加
        ("human", "{input}"),
    ]
)

# Runnableの準備
runnable = prompt_template | llm

# セッションIDごとの会話履歴の取得
store = {}

def get_session_history(session_id: str) -> LimitedChatMessageHistory:
    if session_id not in store:
        store[session_id] = LimitedChatMessageHistory(max_messages=MAX_MESSAGE, max_characters=MAX_CHARACTERS)
    return store[session_id]

# RunnableWithMessageHistoryの準備
runnable_with_history = RunnableWithMessageHistory(
    runnable,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)

# 会話を管理する関数
def chat_with_history(user_input, session_id):
    history = get_session_history(session_id)
    history.add_message(HumanMessage(content=user_input))
    response = runnable_with_history.invoke(
        {"input": user_input},
        config={"configurable": {"session_id": session_id}}
    )
    response_message = AIMessage(content=response.content)
    history.add_message(response_message)
    return response_message.content

# サンプルの会話ループ
if __name__ == "__main__":
    print("End: press 'exit'")
    session_id = "123"  # セッションIDを固定で設定
    while True:
        user_input = input("Human: ")
        if user_input.lower() == 'exit':
            break
        response = chat_with_history(user_input, session_id)
        print(f"AI: {response}")

    # 会話履歴の確認
    if session_id in store:
        print("\n会話履歴:\n", store[session_id].messages)
    else:
        print("\n会話履歴はありません。")
