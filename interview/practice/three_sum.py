"""3Sum learning implementation: unique value triples, distinct indices, target 0."""
from itertools import combinations, product
import random
import sys


def three_sum(nums: list[int]) -> list[tuple[int, int, int]]:
    a = sorted(nums)  # Keep caller's input unchanged.
    result = []
    for i in range(len(a) - 2):
        if i and a[i] == a[i - 1]:
            continue
        if a[i] > 0:
            break
        left, right = i + 1, len(a) - 1
        while left < right:
            total = a[i] + a[left] + a[right]
            if total < 0:
                left += 1
            elif total > 0:
                right -= 1
            else:
                result.append((a[i], a[left], a[right]))
                left += 1
                right -= 1
                while left < right and a[left] == a[left - 1]:
                    left += 1
                while left < right and a[right] == a[right + 1]:
                    right -= 1
    return result


def oracle(nums):
    return {tuple(sorted(c)) for c in combinations(nums, 3) if sum(c) == 0}


def check(nums):
    before = nums.copy()
    actual = three_sum(nums)
    assert nums == before, 'input mutated'
    assert len(actual) == len(set(actual)), 'duplicate result'
    assert set(actual) == oracle(nums), (nums, actual, oracle(nums))


if __name__ == '__main__':
    named = [[], [0], [0, 0], [0, 0, 0], [0, 0, 0, 0], [-1, 0, 1, 2, -1, -4],
             [1, 2, 3], [-3, -2, -1], [-2, 0, 0, 2, 2], [-10**20, 0, 10**20]]
    for values in named:
        check(values)
    exhaustive = 0
    for n in range(8):
        for values in product(range(-2, 3), repeat=n):
            check(list(values))
            exhaustive += 1
    rng = random.Random(20261022)
    for _ in range(1000):
        values = [rng.randint(-20, 20) for _ in range(rng.randint(0, 16))]
        check(values)
        expected = set(three_sum(values))
        shuffled = values.copy(); rng.shuffle(shuffled)
        assert set(three_sum(shuffled)) == expected
        assert set(three_sum([-x for x in values])) == {tuple(sorted(-x for x in t)) for t in expected}
    print('Python:', sys.version.split()[0])
    print(f'PASS: {len(named)} named; {exhaustive} exhaustive arrays; 1000 seeded random arrays; oracle, input preservation, uniqueness and permutation/negation checks')
