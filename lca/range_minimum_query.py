import math
from typing import Callable, Iterable, TypeVar, Tuple

from .protocol import Comparable

V = TypeVar("V")


def build(vs: Iterable[Comparable[V]]) -> Callable[[int, int], int]:
    # """Range Minimum Query based on vs. Returns query function, with arguments [l, r)."""
    n = len(vs)
    n_exp = int(math.floor(math.log2(n)))

    rmq = [[None for _ in range(n)] for _ in range(n_exp + 1)]
    rmq[0] = list(enumerate(vs))
    for j in range(1, n_exp + 1):
        for i in range(0, n + 1 - (1 << j)):
            rmq[j][i] = min(rmq[j-1][i], rmq[j-1][i + (1 << (j-1))], key=lambda iv: iv[1])

    def get_min(l: int, r: int) -> Tuple[int, V]:
        """Min of [l, r). Left inclusive, right exclusive."""
        assert 0 <= l < r <= n
        if (l == r - 1):
            return l, vs[l]
        k = int(math.floor(math.log2(r - 1 - l)))
        return min(rmq[k][l], rmq[k][r - (1 << k)], key=lambda iv: iv[1])

    return get_min
