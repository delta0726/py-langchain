from google.cloud import aiplatform
import vertexai
from vertexai.language_models import ChatModel
from print_color import print

# 利用するモデルの名前を指定 --- (*1)
MODEL_NAME = 'chat-bison@001'
# キャラクターの名前を指定
CHAR_NAME = 'からニャン'
# キャラクターの性格付けをするプロンプト --- (*2)
DEFAULT_PROMPT = f'''
あなたは、ゆるキャラの「{CHAR_NAME}」です。
ユーザーの入力に対して、ユーモアたっぷりに返答してください。
必ず語尾に「にゃん」と加えてください。
それでは、会話を始めるにゃん！
'''

# チャットボットのための初期設定 --- (*3)
aiplatform.init()
chat_model = ChatModel.from_pretrained(MODEL_NAME)
chat_parameters = {
    "max_output_tokens": 256,
    "temperature": 0.5,
}
chat = chat_model.start_chat()
# ボットのキャラクターを設定 --- (*4)
def_response = chat.send_message(DEFAULT_PROMPT, **chat_parameters)
print(def_response.text, color='green', tag=CHAR_NAME)
# チャットを開始 --- (*5)
while True:
    print('--------', color='blue')
    # ユーザーの入力を受け取る --- (*6)
    user = input('[あなた] ')
    if user == 'quit' or user == 'exit': break
    # ユーザーの入力をAPIに送信して返信を表示 --- (*7)
    response = chat.send_message(user, **chat_parameters)
    print(f'{response.text}', tag=CHAR_NAME, color='green')
