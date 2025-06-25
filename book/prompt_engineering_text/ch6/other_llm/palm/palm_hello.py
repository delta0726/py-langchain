from google.cloud import aiplatform
import vertexai
from vertexai.preview.language_models import TextGenerationModel

# 利用するモデルの名前を指定 --- (*1)
MODEL_NAME = 'text-bison@001'

# Vertex AIの認証を行う --- (*2)
aiplatform.init()

# PaLM APIを呼び出す関数 --- (*3)
def call_palm(prompt):
    model = TextGenerationModel.from_pretrained(MODEL_NAME)
    response = model.predict(prompt,
                temperature=0.1,
                max_output_tokens=256)
    return response.text

if __name__ == '__main__':
    # PaLMを呼び出す --- (*4)
    print(call_palm('豚に真珠とはどういう意味ですか？'))

