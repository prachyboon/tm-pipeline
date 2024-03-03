import math
import time

cache_prims = {}


def is_prime(n):
    # 2 is the smallest n
    # 1 is the factor of all n
    # n is the factor of itself
    if cache_prims.get(n):
        return True

    for i in range(2, n):
        if (n % i) == 0:
            return False

    cache_prims[n] = n
    return True


def find_n_prime(a, b):
    i = 0
    running_n = []
    running_n_prims = []
    while True:
        _prime = abs(int(math.pow(i, 2) + (i * a) + b))
        if is_prime(_prime):  # save compute time with cache
            running_n.append(i)
            running_n_prims.append(_prime)
            i = i + 1
        else:
            break  # not consecutive prime ever

    # print("a and b: {} | {}".format(a, b))
    # print("n and length of primes: {} | {}".format((n - 1), list_primes))  # last n is n - 1 that create consecutive
    return running_n, running_n_prims


# time bound: ~ 2000 * 2000 = 4000000
def main():
    max_a, max_b = 0, 0
    max_n, max_primes_n = [], []
    for a in range(-999, 1000):  # TODO: can optimize to O(N) ?
        for b in range(-1000, 1001):
            n, n_primes = find_n_prime(a, b)
            if len(n) > len(max_n):
                max_n = n
                max_primes_n = n_primes
                max_a = a
                max_b = b

    # print("---")
    # print(f"a|b: {max_a}|{max_b} and max_a_dot_b: {max_a * max_b}")
    # print("---")
    return max_n, max_primes_n, (max_a * max_b)


if __name__ == '__main__':
    start = time.time()
    n, primes, dot_ab = main()
    print(f"max n: {n}")
    print(f"max consecutive primes: {primes}")
    print(f"max product a*b: {dot_ab}")
    end = time.time()
    print("elapsed_time: {} s.".format(end - start))
