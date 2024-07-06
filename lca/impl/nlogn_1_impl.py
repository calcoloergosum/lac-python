"""Range minimum query lowest common ancestor by dfs labelling.

preprocessing: O(log n)
query:         O(1)
"""
from typing import Callable, Iterable, Tuple, TypeVar
import math

from .. import range_minimum_query as rmq
from ..protocol import Hashable
from ..graphutil import euler_tour


V = TypeVar("V")
Depth = int


def build(
    root: Hashable[V],
    v2vs: Callable[[Hashable[V]], Iterable[Hashable[V]]]
) -> Callable[[Hashable[V], Hashable[V]], Hashable[V]]:
    # labelling
    tour = list(euler_tour(root, v2vs))
    t2v, t2d = list(zip(*tour))
    v2t = {v: i for i, v in enumerate(t2v)}
    # labelling done

    tt2t = rmq.build(t2d)

    def lca_vv2v(v1: Hashable[V], v2: Hashable[V]) -> V:
        """LCA function with vertex interface"""
        nonlocal v2t, t2v
        if v1 == v2:
            return v1
        t1, t2 = v2t[v1], v2t[v2]
        t1, t2 = min(t1, t2), max(t1, t2)
        t, _ = tt2t(t1, t2 + 1)
        return t2v[t]

    return lca_vv2v
