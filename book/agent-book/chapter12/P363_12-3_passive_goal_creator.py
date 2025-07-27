"""
Title   : LangChainとLangGraphによるRAG・AIエージェント実践入門
Chapter : 12 エージェントデザインパターン
Section : 3 パッシブゴールクリエイター
Theme   : 
Date    : 2025/00/00
Page    : P366-368
"""


# ＜概要＞
# - ユーザーの入力から具体的な目標を抽出するためのパターン
# - ユーザーが自然言語で入力する指示は曖昧でだったり、意図せず複数の目標が含まれたりする
# - エージェントは曖昧な質問を分解して明確な目標に変換する必要がある
# - パッシブゴール・クリエイターはユーザーが提供した情報のみに基づく（過去の行動履歴や外部環境は参照しない）

# ＜プロセス＞
# - 1. ユーザーから入力をテキストで受け取る
# - 2. LLMを用いてテキストから含まれる目標/要求を抽出する
# - 3. 特定された目標を構造化された形式(Pydantic)に変換する
# - 4. 必要に応じて目標の優先順位付けや依存関係の特定を行う
# - 5. 構造化された目標をAIエージェントの次のステップに渡す


from settings import Settings
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field


class Goal(BaseModel):
    description: str = Field(..., description="目標の説明")

    @property
    def text(self) -> str:
        return f"{self.description}"


class PassiveGoalCreator:
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm

    def run(self, query: str) -> Goal:
        prompt = ChatPromptTemplate.from_template(
            template="""
            ユーザーの入力を分析し、明確で実行可能な目標を生成してください。
            要件:
            1. 目標は具体的かつ明確であり、実行可能なレベルで詳細化されている必要があります。
            2. あなたが実行可能な行動は以下の行動だけです。
               - インターネットを利用して、目標を達成するための調査を行う。
               - ユーザーのためのレポートを生成する。
            3. 決して2.以外の行動を取ってはいけません。

            ユーザーの入力: {query}
            """
        )
        chain = prompt | self.llm.with_structured_output(Goal)
        return chain.invoke(input={"query": query})


def main():

    # 環境設定
    settings = Settings()
    
    # LLMの定義
    llm = ChatOpenAI(
        model=settings.openai_smart_model,
        temperature=settings.temperature
    )
    
    # パッシブゴールクリエイターの実行
    # --- 質問を実現するために質問をLLMで掘り下げる
    # --- 質問 ⇒ 明確で実行可能な目標、に変換する
    task_input = "Slack連携のAIアシスタントを作りたい"
    goal_creator = PassiveGoalCreator(llm=llm)
    result = goal_creator.run(query=task_input)
    
    # 結果確認
    print(f"🔎 生成された目標: {result.text}")


if __name__ == "__main__":
    main()