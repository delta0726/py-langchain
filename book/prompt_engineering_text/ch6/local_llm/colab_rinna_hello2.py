from llama_cpp import Llama
# ダウンロードしたモデルを指定
llm = Llama(model_path="rinna-youri-7b-chat-q4_K_S.gguf")
# 関数を定義
def gen_text(prompt):
    prompt = prompt.strip()
    prompt = f'### ユーザー:\n{prompt}\n\n### システム:'
    # 言語モデルから応答を得る
    output = llm(prompt, temperature=1.0, stop=['### ユーザー:', '### システム:'], echo=False)
    return output["choices"][0]["text"]
# 関数を実行
print('-----')
print(gen_text('可愛い白い犬に名前を付けてください。'))
