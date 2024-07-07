import pytest

# import lca.impl.nlogn_1_impl as mod  # 3.75s
import lca.impl.n_1 as mod           # 3.5s
# import lca.impl.n_logn as mod        # 2.5s
import lca.impl.n_logn

from .sample_data import T, v2vs, BinaryTree


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


@pytest.mark.parametrize('tree, v1, v2', [
        # (
        #     (8, 7, 87, (1, 6, 79, (0, 0, 72, None, None), (2, 3, 78, (0, 1, 74, None, (0, 0, 73, None, None)), (1, 1, 77, (0, 0, 75, None, None), (0, 0, 76, None, None)))), (4, 2, 86, (1, 2, 83, (0, 0, 80, None, None), (1, 0, 82, (0, 0, 81, None, None), None)), (1, 0, 85, (0, 0, 84, None, None), None))),
        #     (1, 1, 77, (0, 0, 75, None, None), (0, 0, 76, None, None)),
        #     (0, 0, 76, None, None),
        # ),
        (BinaryTree.random(100), None, None),
        (BinaryTree.random(1000), None, None),
        (BinaryTree.random(10000), None, None),
        (BinaryTree.random(100000), None, None),
    ]
)
def test_random_binary_tree(tree, v1, v2):
    vv2lca = mod.build(tree, BinaryTree.children)
    vv2lca_naive = lca.impl.n_logn.build(tree, BinaryTree.children)

    def _test(v1, v2):
        lca1 = vv2lca(v1, v2)
        lca2 = vv2lca_naive(v1, v2)
        assert lca1 == lca2

    if v1 is not None and v2 is not None:
        _test(v1, v2)

    for _ in range(100000):
        v1 = BinaryTree.choose_random_subtree(tree)
        v2 = BinaryTree.choose_random_subtree(tree)
        _test(v1, v2)
