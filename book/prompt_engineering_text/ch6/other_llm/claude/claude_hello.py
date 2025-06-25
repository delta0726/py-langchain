from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT

# Anthropicのオブジェクトを作成 --- (*1)
anthropic = Anthropic()

# モデル Claude-2 を使ってAPIを呼び出す --- (*2)
def call_claude(prompt):
    # プロンプトを組み立てる --- (*3)
    prompt_text = f'{HUMAN_PROMPT} {prompt}\n\n{AI_PROMPT}'
    # APIを呼び出す --- (*4)
    completion = anthropic.completions.create(
        model='claude-2',
        max_tokens_to_sample=300,
        prompt=prompt_text)
    return completion.completion

# APIを呼び出す --- (*5)
print(call_claude('可愛いネコの名前とその由来を3つ考えてください。'))
