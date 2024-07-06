# Nested tuple as tree
T = ((('a', 'b'), ('c',)), ('d', ('e', 'f')))


def v2vs(v):
    """Children iterator for nested tuple"""
    return v if isinstance(v, tuple) else ()
