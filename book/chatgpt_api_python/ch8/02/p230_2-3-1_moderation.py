from openai import OpenAI

client = OpenAI()

response = client.moderations.create(
    input="こんにちは！"
)
output = response.results[0]

print(output)