def get_prime(num):
    if num < 2:
        return []
    primes = [2]
    for potential_prime in range(3, num, 2):  
        is_prime = True
        for prime in primes:
            dividend, divisor = potential_prime, prime
            # 余りを % 演算子を使わずに求める
            while dividend >= divisor:
                dividend -= divisor
            if dividend == 0:  # 余りが 0 ならば素数ではない
                is_prime = False
                break
        if is_prime:
            primes.append(potential_prime)
    return primes
# テスト
print(get_prime(30))  # [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
