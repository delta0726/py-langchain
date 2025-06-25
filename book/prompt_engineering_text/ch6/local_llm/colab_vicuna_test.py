from llama_cpp import Llama
# ダウンロードしたモデルを指定
llm = Llama(model_path='vicuna-7b-v1.5.Q4_0.gguf')
# プロンプトを指定
prompt = 'Q:日本で一番高い山は？\nA:'
# 言語モデルから応答を得る
output = llm(prompt, temperature=0.1, stop='\n\n', echo=False)
print('-----')
print(output["choices"][0]["text"])
