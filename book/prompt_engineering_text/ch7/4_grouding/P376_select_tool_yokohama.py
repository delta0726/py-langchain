import select_tool_wikipedia as select_tool

if __name__ == '__main__':
    prompt = '横浜市にどれくらい人が住んでいるのでしょうか？'
    res = select_tool.selec_tool(prompt)
    print('=== 結果 ===\n' + res)
