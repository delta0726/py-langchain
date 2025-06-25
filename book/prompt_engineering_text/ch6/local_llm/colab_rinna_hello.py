from llama_cpp import Llama

# ダウンロードしたモデルを指定
llm = Llama(model_path="rinna-youri-7b-chat-q4_K_S.gguf")

# プロンプトを指定
prompt = 'ユーザー:日本で一番高い山は？\nシステム:'

# 言語モデルから応答を得る
output = llm(prompt, temperature=0.1, stop='\n', echo=False)
print('-----')
print(output["choices"][0]["text"])
