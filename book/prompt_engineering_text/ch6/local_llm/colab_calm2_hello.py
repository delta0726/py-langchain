from llama_cpp import Llama

# ダウンロードしたモデルを指定
llm = Llama(model_path="cyberagent-calm2-7b-q4_K_M.gguf")

# プロンプトを指定
prompt = 'USER:日本で一番高い山は？\nASSISTANT:'

# 言語モデルから応答を得る
output = llm(prompt, temperature=0.1, stop='\n', echo=False)
print('-----')
print(output["choices"][0]["text"])
