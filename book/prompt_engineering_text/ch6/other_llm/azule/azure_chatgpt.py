import openai, os

# APIを呼び出す関数 --- (*1)
def call_chatgpt(prompt):
    # Azureの設定を読み込む(環境変数に設定を記述しておく) --- (*2)
    client = openai.AzureOpenAI()
    # APIを呼び出す --- (*3)
    completion = client.chat.completions.create(
        model='test-gpt-35-turbo', # --- (*3a)
        messages=[{'role': 'user', 'content': prompt}])
    return completion.choices[0].message.content

# 実際に動かす --- (*4)
print(call_chatgpt('今日のお昼に食べたい物とその理由を答えてください。'))
