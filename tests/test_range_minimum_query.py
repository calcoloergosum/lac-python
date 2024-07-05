import random

import pytest

import lca.range_minimum_query as rmq


@pytest.mark.parametrize('vs', [
    [i               for i in range(10)],
    [10 - i          for i in range(10)],
    [random.random() for _ in range(10)],
])
def test_rmq(vs):
    N = len(vs)
    get_min_idx = rmq.build(vs)
    for i in range(N):
        for j in range(i + 1, N):
            i_min = get_min_idx(i, j)
            i_min2 = min(range(i, j), key=lambda x: vs[x])
            assert i_min == i_min2
