from typing import Protocol, TypeVar

V = TypeVar("V")


class Hashable(Protocol[V]):
    def __hash__(self: V) -> int:
        ...
        
    def __eq__(self: V, other: V) -> bool:
        ...


class Comparable(Protocol[V]):
    def __eq__(self: V, other: V) -> bool:
        ...

    def __lt__(self: V, other: V) -> bool:
        ...