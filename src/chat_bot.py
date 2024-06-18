from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv
import os

load_dotenv()
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")

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

def get_session_history(session_id: str) -> ChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
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
    print("会話ボットへようこそ！終了するには 'exit' と入力してください。")
    session_id = "123"  # セッションIDを固定で設定
    while True:
        user_input = input("あなた: ")
        if user_input.lower() == 'exit':
            break
        response = chat_with_history(user_input, session_id)
        print(f"ボット: {response}")

    # 会話履歴の確認
    print("\n会話履歴:\n", store[session_id].messages)
