# 2D Arrays (Grids)

**Date:** 2026-02-16
**Status:** In progress - picking up tomorrow

---

## Representation in Python

A grid is a list of lists:
```python
grid: list[list[int]]

grid = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
```

- `grid[i][j]` = row `i`, column `j` (zero-indexed)
- `grid[1][1]` = `5`

---

## Traversing a Grid

Two approaches, both use a nested loop:

**With indices (needed when position matters):**
```python
for i in range(len(grid)):
    for j in range(len(grid[i])):
        print(grid[i][j])
```

**Pythonic (when you just need values):**
```python
for row in grid:
    for cell in row:
        print(cell)
```

Use the index version when you need to know *where* you are (most interview problems). Use the Pythonic version when you just need the values (e.g. summing all elements).

---

## Navigating Neighbors (4-directional)

Given a cell at `(i, j)`, its neighbors are:

| Direction | Coordinates     |
| --------- | --------------- |
| Up        | `(i - 1, j)`   |
| Down      | `(i + 1, j)`   |
| Left      | `(i, j - 1)`   |
| Right     | `(i, j + 1)`   |

### The Directions Array Pattern

Instead of writing 4 separate variables, store the deltas and loop:

```python
directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
#              up       down     left      right

for di, dj in directions:
    neighbor_row = i + di
    neighbor_col = j + dj
```

This scales easily to 8 directions (diagonals) by adding more tuples.

---

## Bounds Checking

Accessing a neighbor without checking bounds will crash on edges/corners.

A neighbor `(neighbor_row, neighbor_col)` is valid when:
```python
neighbor_row >= 0 and neighbor_row < len(grid) and neighbor_col >= 0 and neighbor_col < len(grid[0])
```

- Lower bound: `>= 0` (no negative indices)
- Upper bound: `< len(grid)` for rows, `< len(grid[0])` for columns

---

## Next Session TODO

- [ ] Combine directions array + bounds checking into the `showNeighbors` function
- [ ] Test with corner `(0, 0)` and center `(1, 1)` to verify both cases
- [ ] Move on to a practical grid problem using these building blocks

---

## Exercises Written

- `sumAllElements.py` - basic grid traversal, sum all elements
- `showNeighbors.py` - find neighbors of a cell (needs bounds checking update)
