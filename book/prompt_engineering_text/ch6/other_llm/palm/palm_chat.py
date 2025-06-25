from google.cloud import aiplatform
import vertexai
from vertexai.language_models import ChatModel

# 利用するモデルの名前を指定 --- (*1)
MODEL_NAME = 'chat-bison@001'

# Vertex AIの認証を行う --- (*2)
aiplatform.init()

# チャットのためのオブジェクトを作成 --- (*3)
chat_model = ChatModel.from_pretrained(MODEL_NAME)
chat_parameters = {
    "max_output_tokens": 256,
    "temperature": 0.2,
}
chat = chat_model.start_chat()
# チャットを開始 --- (*4)
print(f'{MODEL_NAME}: チャットを始めましょう!')
while True:
    # ユーザーの入力を受け取る --- (*5)
    user = input('あなた: ')
    if user == 'quit' or user == 'exit': break
    print('--------')
    # ユーザーの入力をAPIに送信して返信を表示 --- (*6)
    response = chat.send_message(user, **chat_parameters)
    print(f'{MODEL_NAME}: {response.text}')
    print('--------')
