# Lowest Common Ancestor in Python

This repository has two implementations.

- `lca.naive::build`:
  - naive and simplest approach
  - $O(n)$ preprocessing time
  - $O(n)$ preprocessing space
  - $O(\log n)$ query time

- `lca.constant_time_linear_space::build`:
  - $O(n)$ preprocessing time
  - $O(n)$ preprocessing space
  - $O(1)$ query time
  - Based on [Wikipedia Article on Lowest common ancestor](https://en.wikipedia.org/wiki/Lowest_common_ancestor). The article has a comprehensive overview on the topic.

## Example Usage

Simply pass the tree and its children iterator.

```python
import lca.constant_time_linear_space as lca_factory

# Nested tuple as tree
T = ((('a', 'b'), ('c',)), ('d', ('e', 'f')))


def v2vs(v):
    """Children iterator for nested tuple"""
    return v if isinstance(v, tuple) else ()


lca = lca_factory.build(T, v2vs)
assert lca(T[0], T[1]) == T
assert lca(T[1], T[0]) == T
assert lca(T[0][0], T[0][0]) == T[0][0]
assert lca(T[0][0], T[0][0][0]) == T[0][0]
assert lca(T[0][0], T[0][1]) == T[0]
assert lca(T[0][0], T[0][1][0]) == T[0]
assert lca(T[0][0], T[1][1][0]) == T
assert lca(T[0][0], T[1][1][1]) == T
assert lca(T[1][0], T[1][1][1]) == T[1]
```
