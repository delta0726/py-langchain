def sieve_of_eratosthenes(limit):
    # 初期化
    primes = [True] * (limit + 1)
    primes[0] = primes[1] = False

    # エラトステネスのふるいを実行
    for current in range(2, int(limit**0.5) + 1):
        if primes[current]:
            for multiple in range(current * current, limit + 1, current):
                primes[multiple] = False

    # 結果を収集
    prime_numbers = [num for num, is_prime in enumerate(primes) if is_prime]

    return prime_numbers

limit = 100
prime_numbers = sieve_of_eratosthenes(limit)

# 結果の出力
print("100以下の素数は以下の通りです:")
print(prime_numbers)
