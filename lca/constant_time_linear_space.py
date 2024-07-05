import itertools
import math
from typing import Callable, Iterable, Tuple, TypeVar

from . import range_minimum_query as rmq
from .constants import VERY_BIG_NUMBER
from .protocol import Hashable

V = TypeVar("V")
Depth = int


def euler_tour(
    root: V,
    v2vs: Callable[[V], Iterable[V]],
    depth_init: int = 0,
) -> Iterable[Tuple[V, Depth]]:
    yield root, depth_init
    for v in v2vs(root):
        yield from euler_tour(v, v2vs, depth_init + 1)
        yield root, depth_init


def build(
    root: Hashable[V],
    v2vs: Callable[[Hashable[V]], Iterable[Hashable[V]]]
) -> Callable[[Hashable[V], Hashable[V]], Hashable[V]]:
    tour = list(euler_tour(root, v2vs))
    n_t = len(tour)
    t2v, t2d = list(zip(*tour))
    v2t = {v: i for i, v in enumerate(t2v)}

    n_per_block_float = math.log(n_t, 2) / 2
    n_b = int(math.ceil(n_t / n_per_block_float))
    block_boundary = [int(math.floor(i * n_per_block_float)) for i in range(n_b + 1)]
    assert block_boundary[-1] >= n_t, f"{block_boundary[-1]} >= {n_t}"
    b2ds = [t2d[i1: i2] for i1, i2 in zip(block_boundary, block_boundary[1:])]
    del n_per_block_float

    # prepare prefix/suffix minimum
    b2t = [0] + cumsum(len(b) for b in b2ds)[:-1]
    b2tmin_prefix = [[] for _ in range(n_b)]
    b2tmin_suffix = [[] for _ in range(n_b)]
    t2b = list(itertools.chain.from_iterable(
        itertools.repeat(bidx, len(b)) for bidx, b in enumerate(b2ds)))

    # sanity check
    assert len(t2b) == len(tour), f"{len(t2b)} != {len(tour)}"
    assert len(b2t) == len(b2ds),   f"{len(b2t)} != {len(b2ds)}"
    # sanity check done

    for i_b, ds in enumerate(b2ds):
        # update prefix
        min_d = VERY_BIG_NUMBER
        min_t_ = None
        for t_, d in enumerate(ds):
            if d <= min_d:
                min_d = d
                min_t_ = t_
            b2tmin_prefix[i_b].append(b2t[i_b] + min_t_)

        # update suffix
        # scan from behind then flip
        min_d = VERY_BIG_NUMBER
        min_t_ = None
        for t_, d in enumerate(ds[::-1]):
            if d <= min_d:
                min_d = d
                min_t_ = t_
            b2tmin_suffix[i_b].append(min_t_)
        # flip!
        b2tmin_suffix[i_b] = [
            (b2t[i_b] + len(ds) - 1 - i)
            for i in b2tmin_suffix[i_b][::-1]
        ]
        # update suffix done

    # Sanity check
    # prepare block minimum should be consistent
    for i_b, (prefix_min, suffix_min) in enumerate(zip(b2tmin_prefix, b2tmin_suffix)):
        assert tour[prefix_min[-1]] == tour[suffix_min[0]]
    # sanity check done

    b2tmin = [prefix_min[-1] for prefix_min in b2tmin_prefix]
    bb2b = rmq.build([t2d[t] for t in b2tmin])

    # inside block
    b2tt2tmin = [[None for _ in ds] for ds in b2ds]
    for b, ds in enumerate(b2ds):
        n_d = len(ds)
        tt2tmin = [
            [
                min(range(t1, t2 + 1), key=lambda t: ds[t])
                if t1 <= t2 else None
                for t2 in range(n_d)
            ]
            for t1 in range(n_d)
        ]
        b2tt2tmin[b] = tt2tmin
    # inside block done

    def lca_tt2t(t1: int, t2: int) -> int:
        """LCA function with vertex interface"""
        nonlocal t2d, t2b, b2tmin, b2tmin_prefix, b2tmin_suffix, bb2b
        t1, t2 = min(t1, t2), max(t1, t2)
        b1, b2 = t2b[t1], t2b[t2]
        if b1 == b2:
            _t = b2t[b1]
            t = b2tt2tmin[b1][t1 - _t][t2 - _t] + _t
            return t

        t1 = b2tmin_suffix[b1][t1 - b2t[b1]]
        t2 = b2tmin_prefix[b2][t2 - b2t[b2]]

        d, t = min((t2d[t1], t1), (t2d[t2], t2))
        if b1 + 1 < b2:
            t_12 = b2tmin[bb2b(b1 + 1, b2)]
            d, t = min((d, t), (t2d[t_12], t_12))
        return t

    def lca_vv2v(v1: Hashable[V], v2: Hashable[V]) -> V:
        """LCA function with vertex interface"""
        nonlocal v2t, t2v
        t1, t2 = v2t[v1], v2t[v2]
        t = lca_tt2t(t1, t2)
        # for _t, v in enumerate(t2v):
        #     print(f"{_t: >3} : {v}")
        return t2v[t]

    return lca_vv2v


def cumsum(ns: Iterable[int]) -> Iterable[int]:
    """Cumulative Sum
    >>> cumsum([1, 2, 3])
    [1, 3, 6]
    """
    ret = [0]
    for n in list(ns):
        ret += [ret[-1] + n]
    return ret[1:]
