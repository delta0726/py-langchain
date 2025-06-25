from llama_cpp import Llama

# ダウンロードしたモデルを指定
llm = Llama(model_path="ELYZA-japanese-Llama-2-7b-fast-instruct-q4_K_M.gguf")

# プロンプトを指定
prompt = '[INST]<<SYS>>あなたは誠実で優秀な日本人のアシスタントです。<</SYS>>' + \
  '可愛いネコの名前を考えて[/INST]'

# 言語モデルから応答を得る
output = llm(prompt, temperature=0.1, stop='\n', echo=False)
print('-----')
print(output["choices"][0]["text"])
