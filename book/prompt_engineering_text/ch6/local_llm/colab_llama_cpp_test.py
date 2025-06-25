from llama_cpp import Llama
# ダウンロードしたモデルを指定 --- (*1)
llm = Llama(model_path='llama-2-7b.Q2_K.gguf')
# プロンプトを指定 --- (*2)
prompt = '日本語で答えてください。\nQ:日本で一番高い山は？\nA:'
# 言語モデルから応答を得る --- (*3)
output = llm(prompt, temperature=0.1, stop='\n', echo=False)
print('-----')
print(output["choices"][0]["text"])
