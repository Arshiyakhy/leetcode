# 200. Number of Islands

**Link:** https://leetcode.com/problems/number-of-islands/
**Difficulty:** Medium
**Topic:** Graph (Grid), Depth-First Search / Breadth-First Search, Matrix Traversal

## Problem

Given an `m x n` 2D grid of `"1"`s (land) and `"0"`s (water), return the
number of **islands** — where an island is a group of `"1"`s connected
horizontally or vertically (not diagonally), surrounded by water.

```
Input:
[["1","1","1","1","0"],
 ["1","1","0","1","0"],
 ["1","1","0","0","0"],
 ["0","0","0","0","0"]]
Output: 1
```

## Why This Is a Graph Problem in Disguise

This doesn't look like a typical "graph" — there's no explicit adjacency
list, no `Node` class. But a **2D grid is a graph**: each cell is a node,
and it has an edge to each of its (up to 4) horizontal/vertical
neighbors. "Count connected groups of land cells" is exactly the same
problem as "count connected components in a graph" — you're just reading
the edges implicitly from grid coordinates instead of an explicit
adjacency list.

Recognizing this equivalence is the single biggest unlock for grid
problems: once you see it as "a graph where neighbors = up/down/left/right
cells," every graph algorithm you know (DFS, BFS, Union-Find) becomes
directly applicable.

## The Key Insight

**Counting connected components** is a two-part strategy:

1. Scan every cell. Whenever you find an unvisited land cell, that's the
   **start of a brand-new island** — increment the island count.
2. From that starting cell, **explore and mark every connected land cell**
   as visited (so the outer scan never counts them again as a "new"
   island).

The DFS in step 2 doesn't need to return anything or compute a value —
its entire job is "flood-fill this island so it disappears from future
consideration." This "flood fill" is a super common DFS/BFS use case, and
step 1 + step 2 together form the standard **connected components**
algorithm template.

## Walkthrough of the Code

```python
directions = [[1, 0], [-1, 0], [0, 1], [0, -1]]
ROWS, COLS = len(grid), len(grid[0])
islands = 0

def dfs(r, c):
    if (r < 0 or c < 0 or r >= ROWS or
        c >= COLS or grid[r][c] == "0"
    ):
        return

    grid[r][c] = "0"
    for dr, dc in directions:
        dfs(r + dr, c + dc)

for r in range(ROWS):
    for c in range(COLS):
        if grid[r][c] == "1":
            dfs(r, c)
            islands += 1

return islands
```

- **`directions`** encodes the 4 possible moves (down, up, right, left) —
  the "edges" of this implicit graph.
- **`dfs(r, c)` — the flood fill:**
  - **Bounds/base case check:** if `(r, c)` is off the grid, _or_ it's
    water (`"0"`), stop exploring this direction. Note this single check
    handles two very different situations (out-of-bounds and
    already-water) with one condition — worth noticing as a clean pattern.
  - **Mark visited by mutating the grid directly:** `grid[r][c] = "0"` —
    this is the clever part. Instead of a separate `visited` set, the
    grid _is_ the visited tracker: once a land cell is explored, it's
    turned into water so it will never be mistaken for unvisited land
    again, either by this DFS call or by the outer scan later.
  - **Recurse in all 4 directions** — explore every neighbor; the base
    case above naturally stops the recursion at the island's boundary.
- **The outer double loop** scans every cell. Every time it finds a `"1"`
  that DFS hasn't already erased, that's a **new** island (since if it
  were part of an already-counted island, DFS would have already turned
  it into `"0"`). Increment `islands` and let `dfs` erase the entire
  connected region so it's never double-counted.

### Trace through a small example

```
1 1 0
0 1 0
0 0 1
```

- `(0,0) = "1"` → new island (`islands = 1`). DFS floods `(0,0), (0,1),
(1,1)` (all connected), turning them to `"0"`.
- Continue scanning: `(0,1)` is now `"0"` (already visited), skip.
  `(0,2) = "0"`, skip. `(1,0) = "0"`, skip. `(1,1)` now `"0"`, skip.
  `(1,2) = "0"`, skip.
- `(2,0) = "0"`, skip. `(2,1) = "0"`, skip.
- `(2,2) = "1"` → new island (`islands = 2`). DFS floods just this single
  cell (no connected neighbors).

Final answer: `2` islands.

## Complexity

- **Time: O(m × n)** — every cell is visited by the outer loop exactly
  once, and every cell is visited by DFS **at most once** total across
  the whole algorithm (since once marked `"0"`, it's never explored
  again). So total work across all DFS calls combined is bounded by the
  total number of cells.
- **Space: O(m × n)** in the worst case — for the recursion call stack, if
  the entire grid is one giant connected island (worst-case recursion
  depth equals the number of land cells). No extra `visited` data
  structure is needed since the grid itself is mutated to track state —
  a nice space-saving trick, though it does mean this solution **destroys
  the input grid** (worth flagging if the caller needs the original grid
  preserved — an alternative would use a separate `visited` set instead
  of mutating `grid`, trading a bit of extra space for not modifying the
  input).

## Pattern to Remember

**"Count connected groups in a grid/graph" → for each unvisited node,
start a DFS/BFS that marks its entire connected component as visited, and
count how many times you had to start a fresh search.**

This is the **connected components** template, and it's foundational for
a huge range of grid and graph problems:

- Number of Islands (this problem)
- Max Area of Island — same DFS, but track and return the size of each
  island instead of just counting them
- Surrounded Regions — flood fill from the _border_ inward, flipping the
  logic slightly
- Number of Provinces — the same idea, but on an explicit adjacency
  matrix instead of a grid
- Pacific Atlantic Water Flow — flood fill from two different starting
  sets of cells, then intersect the results

The "mutate the input to mark visited, instead of a separate visited set"
trick is also broadly reusable whenever you're allowed to modify the
input and don't need to preserve it.

## Edge Cases Handled

- **All water** (`[["0"]]`) — outer loop never finds a `"1"`, `dfs` is
  never called, returns `0`. Correct.
- **Multiple separate islands** (verified via `grid2` test case, expecting
  `3`) — each DFS call only floods its own connected region, so separate
  islands are correctly counted independently.
- **Diagonal-only adjacency does NOT count** — the `directions` list only
  includes the 4 orthogonal moves (no diagonals), matching the problem's
  explicit rule that only horizontal/vertical connections count.

## What I Got Wrong / Things to Watch

_(fill in anything that tripped you up — e.g. did you first try using a
separate `visited` set before realizing you could mutate the grid
directly? Did you consider whether destroying the input grid was
acceptable here?)_
