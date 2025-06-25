from llama_cpp import Llama
# ダウンロードしたモデルを指定
llm = Llama(model_path="cyberagent-calm2-7b-q4_K_M.gguf")
# 関数を定義
def gen_text(prompt):
    prompt = prompt.strip()
    prompt = f'### USER:\n{prompt}\n### ASSISTANT:\n'
    # 言語モデルから応答を得る
    output = llm(prompt, temperature=0.4, stop=['### USER:', '### ASSISTANT:'], echo=False)
    return output["choices"][0]["text"]
# 関数を実行
print('-----')
print(gen_text('灰色で大きな動物と言えば？'))
