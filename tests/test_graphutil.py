from lca import graphutil
from .sample_data import T, v2vs


def test_euler_tour() -> None:
    assert [x for x in graphutil.euler_tour(T, v2vs)] == [
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
