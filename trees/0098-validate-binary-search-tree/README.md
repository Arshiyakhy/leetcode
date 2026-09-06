# 98. Validate Binary Search Tree

**Link:** https://leetcode.com/problems/validate-binary-search-tree/
**Difficulty:** Medium
**Topic:** Binary Search Tree, DFS, Recursion

## Problem

Given the `root` of a binary tree, determine if it is a valid **binary
search tree (BST)**:

- Every node in a node's **left** subtree must have a value **strictly
  less than** that node's value.
- Every node in a node's **right** subtree must have a value **strictly
  greater than** that node's value.
- Both subtrees must themselves also be valid BSTs.

```
Input:  root = [2, 1, 3]
Output: true
```

## The Classic Bug (and why the "obvious" solution is wrong)

The definition above is tempting to implement as "just check each node
against its immediate parent":

```python
# WRONG — only checks the immediate parent, not the whole ancestor chain
def isValidBST(self, root):
    def valid(node, parent_val, is_left):
        if not node:
            return True
        if is_left and node.val >= parent_val:
            return False
        if not is_left and node.val <= parent_val:
            return False
        return valid(node.left, node.val, True) and valid(node.right, node.val, False)
    return valid(root, None, None)
```

This looks reasonable but is **broken**. Consider:

```
        5
      /   \
     1     4
          / \
         3   6
```

Here, `3` is less than its immediate parent `4` (correctly), but `3` is
in the **right subtree of the root `5`** — which means `3` must be
greater than `5`. It isn't. This tree is **not** a valid BST, but a
"check only the direct parent" solution would wrongly say it's valid,
because it never checks `3` against `5` at all — only against `4`.

**The rule "left subtree < node < right subtree" applies to _every_
ancestor, not just the immediate parent.** That's the actual insight this
problem is testing.

## The Key Insight (your solution)

The fix: instead of passing down just "the parent's value," pass down a
**valid range** `(left, right)` that narrows as you descend. Every node
must fall strictly within the range established by _all_ of its
ancestors combined — not just its direct parent.

- The root can be anything: its valid range starts as `(-infinity,
+infinity)`.
- Going **left** from a node tightens the **upper bound**: everything in
  that subtree must be less than the current node's value (the lower
  bound stays whatever it already was, since it came from further up).
- Going **right** tightens the **lower bound**: everything must be
  greater than the current node's value.

This way, a node deep in the tree carries the accumulated constraints of
_every_ ancestor above it, not just its immediate parent.

## Walkthrough of the Code

```python
def isValidBST(self, root):
    def valid(node, left, right):
        if not node:
            return True
        if not (left < node.val < right):
            return False
        return valid(node.left, left, node.val) and valid(node.right, node.val, right)

    return valid(root, float("-inf"), float("inf"))
```

- **Base case:** an empty subtree is trivially valid — nothing to
  violate.
- **Range check:** `left < node.val < right` — this single Python
  chained comparison checks _both_ bounds at once. If the current value
  falls outside the accumulated valid range, the whole tree is invalid
  immediately (short-circuits with `False`, no need to check further).
- **Recurse left:** `valid(node.left, left, node.val)` — the lower bound
  (`left`) is unchanged (still whatever came from above), but the upper
  bound tightens to `node.val`, since everything in the left subtree must
  be less than this node.
- **Recurse right:** `valid(node.right, node.val, right)` — mirror image:
  upper bound unchanged, lower bound tightens to `node.val`.
- **`and` short-circuits:** if the left subtree is already invalid, the
  right subtree is never even checked — Python's `and` stops evaluating
  as soon as it hits a `False`.

### Trace through the broken example above: `[5, 1, 4, null, null, 3, 6]`

```
        5
      /   \
     1     4
          / \
         3   6
```

- `valid(5, -inf, inf)` → `5` is in range. Recurse:
  - Left: `valid(1, -inf, 5)` → `1` is in range (`-inf < 1 < 5`). Both
    children are `None` → `True`.
  - Right: `valid(4, 5, inf)` → is `5 < 4 < inf`? **No** (`4` is not
    greater than `5`). Return `False` immediately.
- Overall: `valid(5,...) and valid(4,...)` → since the right side
  returned `False`, the whole result is `False`.

Correctly identifies the tree as **invalid** — exactly the bug case the
naive "check only direct parent" solution would have missed.

### Trace through a valid tree: `[2, 1, 3]`

- `valid(2, -inf, inf)` → `2` in range. Recurse:
  - Left: `valid(1, -inf, 2)` → `-inf < 1 < 2` ✓. Children `None` → `True`.
  - Right: `valid(3, 2, inf)` → `2 < 3 < inf` ✓. Children `None` → `True`.
- `True and True` → `True`. Correctly valid.

## Complexity

- **Time: O(n)** — every node is visited exactly once, doing O(1) work
  per node (one range comparison).
- **Space: O(h)** — the recursion call stack depth equals the tree's
  height `h` (O(log n) for a balanced tree, O(n) worst case for a
  completely skewed tree).

## Alternative Approach: Inorder Traversal

Since a valid BST's inorder traversal is always strictly increasing (the
same property used in Kth Smallest Element in a BST), you can also
validate a BST by doing an inorder traversal and checking that each value
is strictly greater than the previous one:

```python
def isValidBST(self, root):
    prev = [float("-inf")]

    def inorder(node):
        if not node:
            return True
        if not inorder(node.left):
            return False
        if node.val <= prev[0]:
            return False
        prev[0] = node.val
        return inorder(node.right)

    return inorder(root)
```

Same **O(n) time, O(h) space** — just a different lens on the same
underlying BST property (inorder = sorted). Which one feels more natural
often comes down to whether you're thinking in terms of "valid ranges" or
"sorted sequence."

## Pattern to Remember

**"Validate a property that depends on _all_ ancestors, not just the
immediate parent" → pass down accumulated constraints (a range, a running
value, a set of forbidden values, etc.) through the recursion, tightening
them at each level.**

This range-narrowing technique generalizes well beyond BSTs:

- Validate Binary Search Tree (this problem) — narrow a `(low, high)`
  value range
- Path Sum problems — narrow a "remaining sum needed" as you descend
- Any problem where "check against parent" is tempting but wrong because
  the real constraint comes from higher up the tree

## Edge Cases Handled

- **Single node** (`[1]`) — `valid(1, -inf, inf)` → in range, children
  are `None` → `True`. Any single-node tree is trivially a valid BST.
- **Duplicate values** (`[2, 2, 2]`) — the strict inequality (`left <
node.val < right`, not `<=`) correctly rejects duplicates, since the
  problem requires values to be _strictly_ less/greater, not
  less-than-or-equal.
- **Deeply nested violation** (the `[5, 1, 4, null, null, 3, 6]` example
  above) — correctly caught because the range narrows across every level
  of ancestry, not just the immediate parent.

## What I Got Wrong / Things to Watch

_(fill in anything that tripped you up — e.g. did you initially write the
"check only the parent" version and get bitten by a nested violation test
case? Did you use `<=` instead of `<` at first and fail on duplicate
values?)_
