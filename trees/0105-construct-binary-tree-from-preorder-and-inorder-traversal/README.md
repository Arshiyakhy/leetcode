# 105. Construct Binary Tree from Preorder and Inorder Traversal

**Link:** https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/
**Difficulty:** Medium
**Topic:** Binary Tree, Divide and Conquer, Recursion, Hash Map

## Problem

Given two integer arrays `preorder` and `inorder` representing the
preorder and inorder traversals of the **same** binary tree, reconstruct
and return that tree.

```
Input:  preorder = [3, 9, 20, 15, 7], inorder = [9, 3, 15, 20, 7]
Output: [3, 9, 20, null, null, 15, 7]
```

## The Key Insight

Two facts about these traversals, combined, are exactly enough
information to rebuild the whole tree:

1. **Preorder visits root first**: `preorder[0]` is _always_ the root of
   whatever (sub)tree you're currently building. This tells you **which
   node to create next.**
2. **Inorder visits left subtree, then root, then right subtree**: if you
   find the root's value inside `inorder`, then **everything to its left
   in that array is the entire left subtree**, and **everything to its
   right is the entire right subtree.** This tells you **how to split the
   remaining values between left and right.**

So the algorithm is: pop the next root off the front of `preorder`, find
it in `inorder` to learn the size and membership of the left/right
subtrees, then **recursively repeat the exact same process** on the
appropriately split slices of both arrays.

This is a **divide and conquer** approach: build the root, then delegate
"build the left subtree" and "build the right subtree" to recursive calls
on smaller inputs.

## Walkthrough of the Code (your solution)

```python
def buildTree(self, preorder, inorder):
    if not preorder or not inorder:
        return None

    root = TreeNode(preorder[0])
    mid = inorder.index(preorder[0])
    root.left = self.buildTree(preorder[1:mid + 1], inorder[:mid])
    root.right = self.buildTree(preorder[mid + 1:], inorder[mid + 1:])
    return root
```

- **Base case:** if either array is empty, there's no subtree here —
  return `None`.
- **`root = TreeNode(preorder[0])`** — the first element of `preorder` is
  always the root of the current subtree (fact #1 above).
- **`mid = inorder.index(preorder[0])`** — find where that root sits in
  `inorder`. Everything before index `mid` is the left subtree;
  everything after is the right subtree (fact #2 above).
- **Left recursive call:** `preorder[1:mid+1]` — skip the root itself
  (`preorder[0]`), and take the next `mid` elements. Since preorder always
  visits an entire left subtree before moving to the right subtree, the
  left subtree's preorder values are exactly the next `mid` elements after
  the root. Paired with `inorder[:mid]` (everything left of the root in
  inorder) — both slices describe the same left subtree, just in two
  different traversal orders.
- **Right recursive call:** `preorder[mid+1:]` (everything after the left
  subtree's chunk) paired with `inorder[mid+1:]` (everything right of the
  root) — same logic, mirrored for the right subtree.

### Trace through `preorder = [3, 9, 20, 15, 7]`, `inorder = [9, 3, 15, 20, 7]`

- **Root:** `preorder[0] = 3`. Find `3` in `inorder` → index `1`. So `mid
= 1`: left subtree has `1` node, right subtree has the rest.
- **Left:** `preorder[1:2] = [9]`, `inorder[:1] = [9]` → single-node
  subtree, value `9`.
- **Right:** `preorder[2:] = [20, 15, 7]`, `inorder[2:] = [15, 20, 7]`:
  - Root of this subtree: `20`. Find `20` in `[15, 20, 7]` → index `1`.
  - Left: `preorder[1:2]` of this slice = `[15]`, `inorder[:1]` = `[15]`
    → single node `15`.
  - Right: `preorder[2:]` = `[7]`, `inorder[2:]` = `[7]` → single node `7`.

Resulting tree:

```
        3
      /   \
     9     20
          /  \
         15   7
```

Matches the expected output ✓.

## Complexity (your solution): O(n²)

This is the important catch worth flagging: **this solution is correct,
but not optimal.** Two operations inside the recursion are more expensive
than they look:

- **`inorder.index(preorder[0])`** is a **linear scan** — O(n) in the
  worst case, called once per recursive call (once per node). Across all
  `n` nodes, that's O(n) work × `n` calls = **O(n²)** just for the index
  lookups.
- **The slicing** (`preorder[1:mid+1]`, `inorder[:mid]`, etc.) **copies**
  the sliced portion into a brand-new list every time — also O(n) per
  slice in the worst case, adding more repeated linear-time work on top.

So while each individual line reads as "just find an index" and "just
take a slice," both are secretly O(n) operations happening inside a
recursion that runs O(n) times — that's what pushes the real complexity
to **O(n²)** rather than the O(n) that's actually achievable.

- **Time: O(n²)** (worst case, e.g. a completely skewed tree).
- **Space: O(n²)** worst case too, from all the copied slices across the
  recursion (plus O(h) call stack, dominated by the slicing cost).

## The Optimal O(n) Version

Two fixes address the two costs above:

1. **Precompute a hashmap** of `{value: index in inorder}` once, up
   front — turns `inorder.index(...)` from O(n) into O(1).
2. **Use index pointers into the original arrays instead of slicing** —
   pass `(in_left, in_right)` boundaries as plain integers, and track
   position in `preorder` with a single counter that only ever moves
   forward. This avoids ever copying a sub-array.

```python
def buildTreeOptimal(self, preorder, inorder):
    inorder_index = {val: i for i, val in enumerate(inorder)}
    self.pre_idx = 0

    def helper(in_left, in_right):
        if in_left > in_right:
            return None

        root_val = preorder[self.pre_idx]
        self.pre_idx += 1
        root = TreeNode(root_val)

        mid = inorder_index[root_val]
        root.left = helper(in_left, mid - 1)
        root.right = helper(mid + 1, in_right)
        return root

    return helper(0, len(inorder) - 1)
```

- `self.pre_idx` always points at "the next unused value in `preorder`" —
  since preorder visits root, then entire left subtree, then entire right
  subtree, incrementing this single counter as you go (root first, then
  recursing left, then right) naturally consumes `preorder` in the
  correct order without ever needing to slice it.
- `helper(in_left, in_right)` describes the current subtree using only
  **boundary indices into the original `inorder` array** — no copying.
- `mid - 1` / `mid + 1` narrow the boundaries for the recursive calls,
  exactly mirroring the slicing logic above, but with O(1) arithmetic
  instead of O(n) array copies.

**Time: O(n)** — each node is created exactly once, and every lookup
(`inorder_index[root_val]`) is O(1). **Space: O(n)** — the hashmap, plus
O(h) for the recursion stack (h being tree height).

## Pattern to Remember

**"Reconstruct a tree from two traversal orders" → the first traversal
tells you _what_ to build next (which value is the root), the second
traversal tells you _how to split_ the rest into left/right subtrees.**

And more broadly: **a correct recursive solution can still hide an
accidental O(n) or O(n²) cost inside operations that look "free"** — index
lookups and slicing are the two most common culprits. Always ask "what is
the actual cost of this one line, given how many times this function
recurses?"

Related problems using the same reconstruction idea:

- Construct Binary Tree from Preorder and Inorder Traversal (this
  problem)
- Construct Binary Tree from Inorder and Postorder Traversal — same idea,
  but the "root" comes from the _end_ of postorder instead of the start
  of preorder
- Serialize and Deserialize Binary Tree — a related but distinct
  reconstruction problem, usually solved with a single traversal plus
  explicit null markers instead of two traversals

## Edge Cases Handled

- **Single node** (`preorder = [-1]`, `inorder = [-1]`) — `mid = 0`, both
  recursive calls get empty slices/ranges, correctly returns a single-node
  tree.
- **Empty input** — the base case (`if not preorder or not inorder`) in
  the original solution, or `in_left > in_right` in the optimal version,
  both correctly return `None`.

## What I Got Wrong / Things to Watch

_(worth reflecting on here: did you realize while writing this that
`.index()` and slicing both cost O(n)? This is a very common trap —
the code looks clean and each line looks cheap, but the hidden per-call
cost compounds across the recursion. Good habit going forward: whenever
recursing over an array, ask whether you're passing index bounds or
copying sub-arrays.)_
