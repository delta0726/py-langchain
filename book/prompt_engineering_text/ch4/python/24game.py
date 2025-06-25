import itertools
import operator

# 使用可能な演算子とその文字表現
ops = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,
}

# 式の文字列表現を作る関数
def try_operations(nums):
    for num_perm in itertools.permutations(nums):
        for ops_combo in itertools.product(ops.keys(), repeat=3):
            a, b, c, d = num_perm
            op1, op2, op3 = ops_combo

            # 5つの括り方を全て試す（括弧の組み合わせ）
            expressions = [
                f"(({a}{op1}{b}){op2}{c}){op3}{d}",
                f"({a}{op1}({b}{op2}{c})){op3}{d}",
                f"{a}{op1}(({b}{op2}{c}){op3}{d})",
                f"{a}{op1}({b}{op2}({c}{op3}{d}))",
                f"({a}{op1}{b}){op2}({c}{op3}{d})"
            ]

            for expr in expressions:
                try:
                    if abs(eval(expr) - 24) < 1e-6:
                        return expr
                except ZeroDivisionError:
                    continue
    return None

# テスト入力
numbers = [1, 2, 9, 3]
solution = try_operations(numbers)

if solution:
    print(f"解が見つかりました: {solution} = 24")
else:
    print("解は見つかりませんでした。")