import random

# Nested tuple as tree
T = ((('a', 'b'), ('c',)), ('d', ('e', 'f')))


def v2vs(v):
    """Children iterator for nested tuple"""
    return v if isinstance(v, tuple) else ()
# Nested tuple as tree done


class BinaryTree:
    """Static class"""
    @staticmethod
    def children(tree):
        if tree is None:
            return []
        *_, l, r = tree
        ret = []
        if l is not None:
            ret += [l]
        if r is not None:
            ret += [r]
        return ret

    @staticmethod
    def random(n, i_start: int = 1):
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
        l = BinaryTree.random(n_l, i_start)
        r = BinaryTree.random(n_r, i_start + n_l)

        # Assign left and right subtrees to children
        return (n_l, n_r, i_start + n_l + n_r, l, r)

    @staticmethod
    def choose_random_subtree(tree):
        if tree is None:
            raise RuntimeError
        assert len(tree) == 5
        n_l, n_r, _, l, r = tree
        n = n_l + n_r + 1
        x = random.random()
        if x < n_l / n:
            return BinaryTree.choose_random_subtree(l)
        if x < (n_l + n_r) / n:
            return BinaryTree.choose_random_subtree(r)
        return tree
    # Random binary tree done
