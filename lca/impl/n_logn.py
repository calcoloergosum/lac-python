"""Naive lowest common ancestor by dfs labelling.

preprocessing: O(n)
query:         O(log n)
"""
from typing import Callable, Iterable, TypeVar

from ..protocol import Hashable

V = TypeVar("V")


def build(
    root: Hashable[V],
    v2vs: Callable[[Hashable[V]], Iterable[Hashable[V]]]
) -> Callable[[Hashable[V], Hashable[V]], Hashable[V]]:
    # build label
    i2v = [root]
    v2i = {root: 0}
    i2parent = [None]

    def dfs(v, func):
        for _v in v2vs(v):
            func(v, _v)
            dfs(_v, func)

    def record(v1, v2):
        assert v2 not in v2i
        i = len(i2v)
        i2v.append(v2)
        v2i[v2] = i
        i2parent.append(v2i[v1])
        assert len(i2v) == len(v2i) == len(i2parent), \
            f"{len(i2v)} == {len(v2i)} == {len(i2parent)}"

    dfs(root, record)
    # build label done
    
    def ii2i(i, j):
        if i == j:
            return i
        if j < i:
            return ii2i(j, i)
        if i < j:
            return ii2i(i, i2parent[j])
        raise RuntimeError("Should not be reachable here")

    def vv2v(u, v):
        return i2v[ii2i(v2i[u], v2i[v])]
    return vv2v
