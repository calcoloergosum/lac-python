from .sample_data import BinaryTree


@staticmethod
def test_tree_generation():
    """Check that parent label is smaller than children label"""
    tree = BinaryTree.random(100)
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