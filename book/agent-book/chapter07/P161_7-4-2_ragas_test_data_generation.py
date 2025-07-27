"""
Title   : LangChainとLangGraphによるRAG・AIエージェント実践入門
Chapter : 7 LangSmithを使ったRAGアプリケーションの評価
Section : 4 Ragasによる合成テストデータの生成
Theme   : 
Date    : 2025/06/08
Page    : P161
"""

import nest_asyncio
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from ragas.testset import TestsetGenerator

loader = DirectoryLoader(
    path="./langchain",
    glob="**/*.mdx",
    loader_cls=TextLoader,  # 単純テキストとして読み込み
)

documents = loader.load()
print(len(documents))


for document in documents:
    document.metadata["filename"] = document.metadata["source"]
 

nest_asyncio.apply()

generator = TestsetGenerator.from_langchain(
    llm=ChatOpenAI(model="gpt-4o-mini"),
    embedding_model=OpenAIEmbeddings(),
    knowledge_graph=None,  # 使わない場合は省略可
)

# documents は事前に用意したList[Document]とする
testset = generator.generate_with_langchain_docs(
    documents=documents,
    testset_size=2
)

testset.to_pandas()



from langsmith import Client

dataset_name = "agent-book"

client = Client()

if client.has_dataset(dataset_name=dataset_name):
    client.delete_dataset(dataset_name=dataset_name)

dataset = client.create_dataset(dataset_name=dataset_name)



inputs = []
outputs = []
metadatas = []

for testset_record in testset.test_data:
    inputs.append(
        {
            "question": testset_record.question,
        }
    )
    outputs.append(
        {
            "contexts": testset_record.contexts,
            "ground_truth": testset_record.ground_truth,
        }
    )
    metadatas.append(
        {
            "source": testset_record.metadata[0]["source"],
            "evolution_type": testset_record.evolution_type,
        }
    )
    
    
client.create_examples(
    inputs=inputs,
    outputs=outputs,
    metadata=metadatas,
    dataset_id=dataset.id,
)