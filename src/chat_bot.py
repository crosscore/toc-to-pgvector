from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import RunnablePassthrough
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage

# OpenAI APIキーの設定
openai_api_key = "YOUR_OPENAI_API_KEY"

# OpenAI LLMの初期化
llm = OpenAI(api_key=openai_api_key)

# プロンプトの設定
prompt_template = "次の質問に日本語で答えてください：\n{input}"
prompt = PromptTemplate(input_variables=["input"], template=prompt_template)

# メッセージフィルタ (最近のk個のメッセージ)
def filter_messages(messages, k=10):
    return messages[-k:]

# チェーンの準備
chain = (
    RunnablePassthrough.assign(messages=lambda x: filter_messages(x["messages"]))
    | prompt
    | llm
)

# チャットメッセージ履歴の準備
chat_message_history = ChatMessageHistory()

# コンフィグの準備
config = {"configurable": {"session_id": "abc3"}}

# 会話を管理する関数
def chat_with_history(user_input):
    chat_message_history.add_message(HumanMessage(content=user_input))
    messages = chat_message_history.messages
    response = chain.invoke({"messages": messages, "language": "日本語"}, config=config)
    chat_message_history.add_message(response)
    return response.content

# サンプルの会話ループ
if __name__ == "__main__":
    print("会話ボットへようこそ！終了するには 'exit' と入力してください。")
    while True:
        user_input = input("あなた: ")
        if user_input.lower() == 'exit':
            break
        response = chat_with_history(user_input)
        print(f"ボット: {response}")
