import math
from typing import Callable, Iterable, TypeVar

from .constants import VERY_BIG_NUMBER
from .protocol import Comparable

V = TypeVar("V")


def build(vs: Iterable[Comparable[V]]) -> Callable[[int, int], int]:
    """Range Minimum Query based on vs. Returns query function, with arguments [l, r)."""
    n = len(vs)
    n_exp = int(math.ceil(math.log(n, 2)))

    # vs[B[i, j]] = min(vs[i:i+2**j])
    B = [[VERY_BIG_NUMBER for _ in range(n_exp)] for _ in range(n)]
    for i in range(n):
        B[i][0] = i
    for j in range(1, n_exp):
        for i in range(n):
            l = B[i][j-1]
            assert vs[l] == min(vs[i: i + 2 ** (j - 1)]), f"{i}, {j - 1}"
            i_r = i + 2**(j - 1)
            if i_r >= n:
                assert vs[l] == min(vs[i: i + 2 ** j])
                B[i][j] = l
                continue

            r = B[i_r][j-1]
            if r == VERY_BIG_NUMBER or vs[l] <= vs[r]:
                assert vs[l] == min(vs[i: i + 2 ** j])
                B[i][j] = l
                continue
            assert vs[r] == min(vs[i: i + 2 ** j]), f"{i}, {j}"
            B[i][j] = r
        
    def get_min(l: int, r: int) -> int:
        """Min of [l, r). Left inclusive, right exclusive."""
        # Calculate min(min(vs[l: l + 2 ** d]), min(vs[r - 2 ** d: r]))
        #         = min(vs[B[l][d]], vs[B[r - 2 ** d][d]])
        # where d = log r - l
        nonlocal B, n
        assert 0 <= l < r <= n
        w = r - l
        logw = int(math.ceil(math.log(w + 1, 2)) - 1)
        assert l + 2 ** logw <= r
        assert l <= r - 2 ** logw
        i_l, i_r = B[l][logw], B[r - 2 ** logw][logw]
        i = i_l if vs[i_l] <= vs[i_r] else i_r
        i_debug = min(enumerate(vs[l: r]), key=lambda x: x[1])[0] + l
        assert i == i_debug, f"{i} != {i_debug} == min(vs[{l}:{r}])"
        return i

    return get_min
