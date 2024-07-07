from tests.sample_data import BinaryTree
import contextlib
from typing import Callable
import time
import lca.impl.nlogn_1_impl
import lca.impl.n_1
import lca.impl.n_logn


@contextlib.contextmanager
def timer(on_end: Callable[[float], None]):
    start = time.time()
    yield
    end = time.time()
    on_end(end - start)
    return


def main():
    for mod in [
        lca.impl.nlogn_1_impl,
        lca.impl.n_1,
        lca.impl.n_logn,
    ]:
        for n in [2 ** (10 + n) for n in range(10)]:
            n_node, n_query = n, n
            t_overhead = 0.
            t_build = 0.
            t_run = 0.

            # prepare timers
            def on_overhead(t):
                nonlocal t_overhead
                t_overhead += t

            def on_build(t):
                nonlocal t_build
                t_build += t

            def on_run(t):
                nonlocal t_run
                t_run += t
            # prepare timer done

            with timer(on_overhead):
                tree = BinaryTree.random(n_node)

            with timer(on_build):
                vv2lca = mod.build(tree, BinaryTree.children)

            # run
            for _ in range(n_query):
                with timer(on_overhead):
                    v1 = BinaryTree.choose_random_subtree(tree)
                    v2 = BinaryTree.choose_random_subtree(tree)
                with timer(on_run):
                    vv2lca(v1, v2)
            # run done
            
            # report
            print("Overhead", mod.__name__, n_node, n_query, t_overhead)
            print("Build", mod.__name__, n_node, n_query, t_build)
            print("Query", mod.__name__, n_node, n_query, t_run)


if __name__ == '__main__':
    main()
