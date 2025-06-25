"""
Title   : Chatgpt API & Python
Section : 5 最新情報を含めたニュース記事を作ろう
Theme   : 最新ニュースの取得をGoogle経由で行うためエージェントを活用する
Date    : 2025/05/05
Page    : P196
"""

from langchain.tools import Tool
from langchain_google_community import GoogleSearchAPIWrapper
from langchain.prompts import PromptTemplate
from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI

"""
質問：2023年のWBCの優勝国について
"""


def create_prompt(user_input):
    prompt = PromptTemplate(
        input_variables=["theme"],
        template="""
        あなたはニュース記事を書くブロガーです。
        下記のテーマについて、Google検索で最新情報を取得し、取得した情報にもとづいてニュース記事を書いてください。
        1000文字以上で、日本語で出力してください。
        記事の末尾に参考にしたURLを参照元としてタイトルとURLを出力してください。
        ###
        テーマ：{theme}
        """,
    )
    return prompt.format(theme=user_input)


def define_tools():
    """
    Agentに渡すためのツール
     - エージェントはdescriptionを見てツールを判断するため正確な記述が必要
    """
    search = GoogleSearchAPIWrapper()
    return [
        Tool(
            name="Search",
            func=search.run,
            description="最新情報を取得するための検索ツールです。質問に関連するキーワードで検索してください。",
        ),
    ]


def write_response_to_file(response, filename):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(response)
    print("出力が完了しました")


def main():
    # LLMの設定
    llm = ChatOpenAI(temperature=0, model="gpt-4o-mini", max_tokens=2000)

    # Agentツールの設定
    tools = define_tools()

    # エージェントの定義
    # --- toolとLLMを持たせる
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.OPENAI_FUNCTIONS,
        verbose=True,
    )

    # 問い合わせ
    prompt = create_prompt(input("記事のテーマを入力してください： "))
    response = agent.run(prompt)

    # 結果出力
    write_response_to_file(response, "result/output.txt")


if __name__ == "__main__":
    main()
