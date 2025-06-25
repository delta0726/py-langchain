import boto3
import json

# Bedrock APIを使うためのクライアントを作成 --- (*1)
client = boto3.client('bedrock-runtime')

# Bedrock APIを呼び出す関数を定義 --- (*2)
def call_bedrock(prompt):
    # パラメーターを生成 --- (*3)
    body = {
        'prompt': f'\n\nHuman:{prompt}\n\nnAssistant:',
        'max_tokens_to_sample': 300,
    }
    # APIを呼び出す --- (*4)
    response = client.invoke_model(
        modelId='anthropic.claude-instant-v1',
        body=json.dumps(body),
        accept='application/json',
        contentType='application/json')
    # 戻り値を得る --- (*5)
    body_json = response.get('body').read()
    completion = json.loads(body_json).get('completion')
    return completion

# 関数を呼び出す --- (*6)
print(call_bedrock('人はなぜ山に登るのですか？100文字以内で答えてください。'))
