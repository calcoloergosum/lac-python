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
    mods = [
        lca.impl.nlogn_1_impl,
        lca.impl.n_1,
        # lca.impl.n_logn,
    ]
    modname2result = {m.__name__: [] for m in mods}
    n2tree = {}
    ns = [4 ** (5 + n) for n in range(6)]
    for n in ns:
        t_overhead = 0.
        def on_overhead(t):
            nonlocal t_overhead
            t_overhead += t
        with timer(on_overhead):
            tree = BinaryTree.random(n)
        n2tree[n] = t_overhead, tree

    for mod in mods:
        for n in ns:
            n_node, n_query = n, n
            t_build = 0.
            t_query = 0.

            # prepare timers
            def on_build(t):
                nonlocal t_build
                t_build += t

            def on_run(t):
                nonlocal t_query
                t_query += t
            # prepare timer done
            t_overhead, tree = n2tree[n]

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
            modname2result[mod.__name__].append((n_node, n_query, t_build, t_query))
            print("Overhead", mod.__name__, n_node, n_query, t_overhead)
            print("Build",    mod.__name__, n_node, n_query, t_build)
            print("Query",    mod.__name__, n_node, n_query, t_query)
    plot(modname2result)


def plot(modname2result):
    import matplotlib.pyplot as plt
    plt.title("Lowest Common Ancester Algorithm Benchmark")
    _, (ax_build, ax_query) = plt.subplots(2)
    
    # plot build
    ax_build.set_xlabel("#nodes")
    ax_build.set_ylabel("Build Time")
    for name, results in modname2result.items():
        if len(results) == 0:
            continue
        ns, _, ts, _ = list(zip(*results))
        ax_build.plot(ns, ts, label=name)
    ax_build.legend()
    # plot build done

    # plot query
    ax_query.set_xlabel("#nodes")
    ax_query.set_ylabel("Query Time")
    for name, results in modname2result.items():
        if len(results) == 0:
            continue
        _, ns, _, ts = list(zip(*results))
        ax_query.plot(ns, ts, label=name, marker='o')
    ax_query.legend()
    # plot query done

    plt.show()


if __name__ == '__main__':
    main()
