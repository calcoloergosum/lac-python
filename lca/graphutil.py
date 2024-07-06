from typing import Callable, Iterable, Tuple, TypeVar


V = TypeVar("V")
Depth = int


def euler_tour(
    root: V,
    v2vs: Callable[[V], Iterable[V]],
    depth_init: Depth = 0,
) -> Iterable[Tuple[V, Depth]]:
    yield root, depth_init
    for v in v2vs(root):
        yield from euler_tour(v, v2vs, depth_init + 1)
        yield root, depth_init
