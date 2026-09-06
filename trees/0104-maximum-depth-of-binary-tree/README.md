# 104. Maximum Depth of Binary Tree

**Link:** https://leetcode.com/problems/maximum-depth-of-binary-tree/
**Difficulty:** Easy
**Topic:** Binary Tree, DFS, BFS, Recursion

## Problem

Given the `root` of a binary tree, return its maximum depth — the number
of nodes along the longest path from the root down to the farthest leaf.

```
Input:  root = [3, 9, 20, null, null, 15, 7]
Output: 3
```

## The Key Insight

"Maximum depth" has a beautifully simple **recursive definition**:

> The depth of a tree is `1` (for the current node) `+` the depth of
> whichever subtree (left or right) is deeper.

And the base case is just as simple: an empty tree (`None`) has depth
`0`. This recursive structure is what makes trees so naturally suited to
recursive (DFS) solutions — the answer for the whole tree is built
directly from the answers to its (smaller) subtrees.

There isn't really a "brute force vs. optimized" distinction here the way
there was for array problems — the recursive definition above **is** the
optimal solution. What's genuinely useful is seeing the **three different
ways** to implement that same idea, since each reflects a different
traversal strategy you'll reuse constantly on tree problems.

## Approach 1 — Recursive DFS (your solution)

```python
def maxDepth(self, root):
    if not root:
        return 0
    return 1 + max(self.maxDepth(root.left), self.maxDepth(root.right))
```

- **Base case:** an empty subtree has depth `0`.
- **Recursive case:** compute the depth of the left subtree and the right
  subtree independently, take whichever is bigger, and add `1` for the
  current node itself.
- This directly mirrors the recursive definition above — it's the most
  natural way to express "depth" once you see the tree as defined in
  terms of its subtrees.

### Trace through `[3, 9, 20, null, null, 15, 7]`

```
        3
      /   \
     9     20
          /  \
         15   7
```

- `maxDepth(9)` = `1 + max(maxDepth(None), maxDepth(None))` = `1 + max(0,
0)` = `1`
- `maxDepth(15)` = `1`, `maxDepth(7)` = `1`
- `maxDepth(20)` = `1 + max(maxDepth(15), maxDepth(7))` = `1 + max(1, 1)`
  = `2`
- `maxDepth(3)` = `1 + max(maxDepth(9), maxDepth(20))` = `1 + max(1, 2)`
  = `3`

Final answer: `3` ✓ (path `3 -> 20 -> 15` or `3 -> 20 -> 7`).

**Time: O(n)** — every node visited once. **Space: O(h)** — the call
stack depth equals the tree's height `h` (worst case O(n) for a
completely unbalanced/skewed tree, best case O(log n) for a balanced
tree).

## Approach 2 — Iterative BFS (Level-Order Traversal)

```python
def maxDepthBFS(self, root):
    if not root:
        return 0

    level = 0
    q = deque([root])
    while q:
        for _ in range(len(q)):
            node = q.popleft()
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
        level += 1
    return level
```

- Instead of thinking "depth of subtree," this thinks **"how many full
  levels does this tree have?"** — which is exactly the same number, just
  computed differently.
- `q` holds all nodes at the **current level**. The `for _ in
range(len(q))` trick is the key idiom here: by snapshotting `len(q)`
  _before_ the loop starts appending children, the loop processes exactly
  one level's worth of nodes at a time, even though `q` is growing as it
  goes.
- Each full pass through the `for` loop = one complete level processed →
  increment `level` once per pass, not once per node.
- This is the standard **level-order traversal** template — you'll reuse
  the "snapshot `len(q)`, process that many nodes, then move to the next
  level" pattern any time a problem asks about _levels_ specifically
  (not just DFS depth).

**Time: O(n)** — every node still visited exactly once. **Space: O(w)** —
where `w` is the tree's maximum **width** (the most nodes at any single
level), since that's the largest the queue ever gets. For a wide, shallow
tree this can be worse than the DFS version's O(h); for a narrow, deep
tree it's much better.

## Approach 3 — Iterative DFS (Explicit Stack)

```python
def maxDepthIterativeDFS(self, root):
    if not root:
        return 0

    stack = [(root, 1)]
    result = 0
    while stack:
        node, depth = stack.pop()
        result = max(result, depth)
        if node.left:
            stack.append((node.left, depth + 1))
        if node.right:
            stack.append((node.right, depth + 1))
    return result
```

- This simulates Approach 1's recursion **manually**, using an explicit
  stack of `(node, depth)` pairs instead of relying on Python's call
  stack.
- Each time a node is popped, its depth is compared against the running
  `result`; its children are pushed with `depth + 1`.
- Functionally equivalent to Approach 1, but useful to know because deep
  recursion can hit Python's recursion limit on very unbalanced trees —
  converting recursion to an explicit stack sidesteps that risk while
  keeping the same DFS traversal order (just not strictly the same
  left-to-right visiting order, since stacks pop LIFO).

**Time: O(n)**. **Space: O(h)** — same as Approach 1, since the stack
holds at most one root-to-leaf path's worth of pending nodes at a time
(same order of magnitude as the recursive call stack).

## Comparing All Three

| Approach              | Time | Space | Best suited for                                                  |
| --------------------- | ---- | ----- | ---------------------------------------------------------------- |
| Recursive DFS         | O(n) | O(h)  | Simplest to write; risk of recursion limit on deep/skewed trees  |
| Iterative BFS         | O(n) | O(w)  | When the problem is naturally about _levels_ (not just this one) |
| Iterative DFS (stack) | O(n) | O(h)  | Same behavior as recursive DFS, without using the call stack     |

For _this specific problem_, all three give the same answer and the same
asymptotic time complexity — the choice mostly comes down to which
traversal style the rest of a larger problem needs, or whether recursion
depth is a practical concern.

## Pattern to Remember

**Tree problems almost always reduce to "define the answer for a node in
terms of the answer for its children" → recursive DFS is usually the
most natural fit, but BFS (level-order) is the right tool whenever the
question is specifically about levels/layers rather than depth in the
abstract.**

Related problems building on these same three templates:

- Maximum Depth of Binary Tree (this problem)
- Minimum Depth of Binary Tree — same recursive shape, but `min` instead
  of `max`, with a subtlety around nodes with only one child
- Binary Tree Level Order Traversal — the BFS template above, but
  collecting each level's values instead of just counting
- Balanced Binary Tree — recursive DFS, but check the height difference
  between subtrees at every node, not just compute a single depth

## Edge Cases Handled

- **Empty tree** (`root = None`) — all three approaches explicitly check
  for this and return `0` immediately.
- **Single node** (`[1]`) — depth `1`, works correctly in all three
  (no children to recurse/queue/push).
- **Skewed tree, only right children** (`[1, null, 2]`) — depth `2`;
  verified via test case. This is also the case where recursive/iterative
  DFS use O(n) space (since `h = n` for a fully skewed tree), while BFS
  would use only O(1) space (since `w = 1` at every level) — a good
  illustration of when each approach's space complexity actually matters
  in practice.

## What I Got Wrong / Things to Watch

_(fill in anything that tripped you up — e.g. had you seen the `for _ in
range(len(q))` level-order trick before? Would you reach for iterative
DFS over recursive DFS if you were worried about a very deep/skewed
tree?)\_
