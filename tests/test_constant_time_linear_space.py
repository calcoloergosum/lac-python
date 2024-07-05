import itertools
import random

import pytest

import lca.constant_time_linear_space as mod
import lca.naive


# Nested tuple as tree
T = ((('a', 'b'), ('c',)), ('d', ('e', 'f')))


def v2vs(v):
    """Children iterator for nested tuple"""
    return v if isinstance(v, tuple) else ()


def test_euler_tour() -> None:
    assert [x for x in mod.euler_tour(T, v2vs)] == [
        (T, 0),
        (T[0], 1),
        (T[0][0], 2),
        (T[0][0][0], 3),
        (T[0][0], 2),
        (T[0][0][1], 3),
        (T[0][0], 2),
        (T[0], 1),
        (T[0][1], 2),
        (T[0][1][0], 3),
        (T[0][1], 2),
        (T[0], 1),
        (T, 0),
        (T[1], 1),
        (T[1][0], 2),
        (T[1], 1),
        (T[1][1], 2),
        (T[1][1][0], 3),
        (T[1][1], 2),
        (T[1][1][1], 3),
        (T[1][1], 2),
        (T[1], 1),
        (T, 0),
    ]


def test_lca():
    """Some simple testcases"""
    _lca = mod.build(T, v2vs)
    assert _lca(T[0], T[1]) == T
    assert _lca(T[1], T[0]) == T
    assert _lca(T[0][0], T[0][0]) == T[0][0]
    assert _lca(T[0][0], T[0][0][0]) == T[0][0]
    assert _lca(T[0][0], T[0][1]) == T[0]
    assert _lca(T[0][0], T[0][1][0]) == T[0]
    assert _lca(T[0][0], T[1][1][0]) == T
    assert _lca(T[0][0], T[1][1][1]) == T
    assert _lca(T[1][0], T[1][1][1]) == T[1]


# Randomized test
def tree_binary_random(n, i_start: int = 1):
    """Generate random binary tree.
    Parent label is smaller than children label
    """
    if n == 0:
        return None
    assert n >= 1

    # Choose random sizes for left and right subtrees
    n_l = random.randint(0, n - 1)
    n_r = n - 1 - n_l
    assert n_l + n_r == n - 1

    # Generate left and right subtrees recursively
    l = tree_binary_random(n_l, i_start)
    r = tree_binary_random(n_r, i_start + n_l)

    # Assign left and right subtrees to children
    return (n_l, n_r, i_start + n_l + n_r, l, r)


def test_tree_generation():
    """Check that parent label is smaller than children label"""
    tree = tree_binary_random(100)
    depth = 0
    depth2maxlabel = {}

    def dfs(tree, func):
        if tree is None:
            return
        *_, data, l, r = tree
        func(data)
        dfs(l, func)
        dfs(r, func)

    def func(data):
        nonlocal depth
        assert depth2maxlabel.get(depth, 0) < data
    dfs(tree, func)


def choose_random_subtree(tree):
    if tree is None:
        raise RuntimeError
    assert len(tree) == 5
    n_l, n_r, _, l, r = tree
    n = n_l + n_r + 1
    x = random.random()
    if x < n_l / n:
        return choose_random_subtree(l)
    if x < (n_l + n_r) / n:
        return choose_random_subtree(r)
    return tree


def flatten(tree):
    """
    >>> tree = tree_binary_random(100)
    >>> sorted(flatten(tree)) == list(range(1, 101))
    True
    """
    if tree is None:
        return [None]
    *_, name, l, r = tree
    return filter(lambda x: x is not None, itertools.chain([name], flatten(l), flatten(r)))


@pytest.mark.parametrize('tree, v1, v2', [
        # (
        #     (8, 7, 87, (1, 6, 79, (0, 0, 72, None, None), (2, 3, 78, (0, 1, 74, None, (0, 0, 73, None, None)), (1, 1, 77, (0, 0, 75, None, None), (0, 0, 76, None, None)))), (4, 2, 86, (1, 2, 83, (0, 0, 80, None, None), (1, 0, 82, (0, 0, 81, None, None), None)), (1, 0, 85, (0, 0, 84, None, None), None))),
        #     (1, 1, 77, (0, 0, 75, None, None), (0, 0, 76, None, None)),
        #     (0, 0, 76, None, None),
        # ),
        (tree_binary_random(100), None, None),
        (tree_binary_random(100), None, None),
        (tree_binary_random(100), None, None),
    ]
)
def test_random_binary_tree(tree, v1, v2):
    def v2vs(tree):
        if tree is None:
            return []
        *_, l, r = tree
        ret = []
        if l is not None:
            ret += [l]
        if r is not None:
            ret += [r]
        return ret

    vv2lca = mod.build(tree, v2vs)
    vv2lca_naive = lca.naive.build(tree, v2vs)

    def _test(v1, v2):
        lca1 = vv2lca(v1, v2)
        lca2 = vv2lca_naive(v1, v2)
        assert lca1 == lca2

    if v1 is not None and v2 is not None:
        _test(v1, v2)

    for _ in range(100):
        v1 = choose_random_subtree(tree)
        v2 = choose_random_subtree(tree)
        _test(v1, v2)
