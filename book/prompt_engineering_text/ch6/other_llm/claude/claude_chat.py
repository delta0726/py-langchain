from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT

# Anthropicのオブジェクトを作成 --- (*1)
anthropic = Anthropic()
chat_logs = []

# モデル Claude-2 を使ってAPIを呼び出す --- (*2)
def call_claude_chat(prompt):
    # プロンプトを組み立てる --- (*3)
    prompt_line = f'{HUMAN_PROMPT} {prompt}'
    # 過去ログに今回のプロンプトを追加
    chat_logs.append(prompt_line)
    # Claudeに送信するプロンプトを組み立てる --- (*4)
    prompt_text = '\n\n'.join(chat_logs) + '\n\n' + AI_PROMPT
    # APIを呼び出す --- (*5)
    completion = anthropic.completions.create(
        model='claude-2',
        max_tokens_to_sample=300,
        prompt=prompt_text)
    # 過去ログに応答を追加 --- (*6)
    res_line = f'{AI_PROMPT} {completion.completion}'
    chat_logs.append(res_line)
    return completion.completion

# チャットを行う --- (*7)
print('Claude 2とチャットをしましょう。')
while True:
    print('---------')
    # ユーザーからの入力を受け付ける --- (*8)
    user = input('あなた: ')
    # ユーザーが「quit」と入力したら終了
    if user == 'quit' or user == 'exit': break
    print('---------')
    # ユーザーの入力をプロンプトにしてAPIを呼び出す --- (*9)
    response = call_claude_chat(user)
    # APIの応答を表示
    print('Claude: ' + response)
