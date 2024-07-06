import random

import pytest

import lca.range_minimum_query as rmq


@pytest.mark.parametrize('vs', [
    # list(range(10)),
    list(reversed(list(range(10)))),
    [random.random() for _ in range(10)],
    [random.random() for _ in range(100)],
])
def test_rmq(vs):
    n = len(vs)
    get_min = rmq.build(vs)
    for l in range(n - 1):
        for r in range(l + 1, n):
            _, min_pred = get_min(l, r)
            min_gt = min(vs[l:r])
            assert min_pred == min_gt, f"{min_pred} == {min_gt} range [{l}, {r}) of {vs}"
