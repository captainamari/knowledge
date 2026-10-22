"""Non-negative integer heights, unit-width bars; no mutation of input."""
from itertools import product
from random import Random
import sys


def trap(height: list[int]) -> int:
    left, right = 0, len(height) - 1
    left_max = right_max = 0
    volume = 0
    while left <= right:
        if left_max <= right_max:
            left_max = max(left_max, height[left])
            volume += left_max - height[left]
            left += 1
        else:
            right_max = max(right_max, height[right])
            volume += right_max - height[right]
            right -= 1
    return volume


def oracle(h: list[int]) -> int:
    return sum(min(max(h[:i+1]), max(h[i:])) - x for i, x in enumerate(h))


def run_tests() -> None:
    examples = [([], 0), ([0], 0), ([1, 2], 0), ([3, 2, 1], 0),
                ([2, 2, 2], 0), ([2, 0, 2], 2), ([4, 2, 0, 3, 2, 5], 9),
                ([0,1,0,2,1,0,1,3,2,1,2,1], 6), ([10**12, 0, 10**12], 10**12)]
    for h, expected in examples:
        original = h.copy()
        assert trap(h) == expected, (h, expected, trap(h))
        assert h == original
    exhaustive = 0
    for n in range(8):
        for items in product(range(4), repeat=n):
            h = list(items)
            assert trap(h) == oracle(h), h
            exhaustive += 1
    rng = Random(20261022)
    for _ in range(1000):
        h = [rng.randrange(100) for _ in range(rng.randrange(100))]
        v = trap(h)
        assert v == oracle(h)
        assert trap(h[::-1]) == v
        assert trap([x + 7 for x in h]) == v
        assert trap([x * 3 for x in h]) == v * 3
    print('Python:', sys.version.split()[0])
    print(f'PASS: {len(examples)} named cases; {exhaustive} exhaustive arrays; 1000 seeded random arrays with oracle + 3 metamorphic checks each')


if __name__ == '__main__':
    run_tests()
