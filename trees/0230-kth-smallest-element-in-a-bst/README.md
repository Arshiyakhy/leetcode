# 230. Kth Smallest Element in a BST

**Link:** https://leetcode.com/problems/kth-smallest-element-in-a-bst/
**Difficulty:** Medium
**Topic:** Binary Search Tree, Depth-First Search (Inorder Traversal)

## Problem

Given the root of a **binary search tree (BST)** and an integer `k`,
return the `k`-th smallest value among all node values in the tree
(1-indexed).

```
Input:  root = [3, 1, 4, null, 2], k = 1
Output: 1
```

## The Key Property of a BST (why this problem isn't "just any tree")

A BST has a defining rule: for every node, everything in its **left**
subtree is smaller, and everything in its **right** subtree is larger.

This one property means there's a traversal order that visits every node
**in fully sorted order, for free** — no sorting step required:

> **Inorder traversal** (left subtree → node → right subtree) of a BST
> always visits nodes in strictly increasing order.

This is the single most important fact about BSTs to have memorized —
almost every "find the k-th / find the median / find values in a range"
BST problem reduces to "do an inorder traversal, then do something simple
with the resulting sorted sequence."

## Walkthrough of the Code

```python
def inorder(self, root):
    result = []

    def _traverse(node):
        if node is None:
            return
        _traverse(node.left)
        result.append(node.val)
        _traverse(node.right)

    _traverse(root)
    return result

def kthSmallest(self, root, k):
    result = self.inorder(root)
    return result[k - 1]
```

- **`_traverse` is a classic recursive inorder DFS:**
  1. **Base case:** if `node` is `None`, there's nothing to visit — return.
  2. **Recurse left first** — fully explore everything smaller before
     touching the current node.
  3. **Visit the current node** — append its value to `result`. Because
     step 2 already handled everything smaller, this is exactly the right
     moment to record this value in sorted position.
  4. **Recurse right** — explore everything larger, after the current
     node has already been recorded.
- After the full traversal, `result` is the **entire tree, sorted**, as a
  flat list.
- `kthSmallest` then just indexes into that sorted list: `result[k - 1]`
  (converting the 1-indexed `k` from the problem into Python's 0-indexed
  list access).

### Trace through `[3, 1, 4, null, 2]` (tree from the example)

```
        3
      /   \
     1     4
      \
       2
```

Inorder traversal order:

1. Go left from `3` → arrive at `1`.
2. Go left from `1` → `None`, return.
3. Visit `1` → `result = [1]`.
4. Go right from `1` → arrive at `2`.
5. Visit `2` → `result = [1, 2]`.
6. Back at `3` → visit it → `result = [1, 2, 3]`.
7. Go right from `3` → arrive at `4`.
8. Visit `4` → `result = [1, 2, 3, 4]`.

Final `result = [1, 2, 3, 4]` — fully sorted, exactly as guaranteed by the
inorder-on-a-BST property. For `k = 1`: `result[0] = 1` ✓.

## Complexity

- **Time: O(n)** — every node is visited exactly once during the
  traversal, regardless of `k`.
- **Space: O(n)** — `result` stores every node's value, plus the
  recursion call stack (up to O(h) where `h` is the tree height, worst
  case O(n) for a completely unbalanced tree).

## A More Efficient Alternative (worth knowing)

Your solution always visits the **entire** tree, even when `k` is small.
If the tree has a million nodes and `k = 1`, you're still doing a full
O(n) traversal and building a full O(n) list just to read the very first
element. An **early-stopping inorder traversal** fixes this by tracking a
counter and stopping the moment the k-th node is found:

```python
def kthSmallest(self, root, k):
    stack = []
    curr = root
    count = 0

    while stack or curr:
        while curr:
            stack.append(curr)
            curr = curr.left
        curr = stack.pop()
        count += 1
        if count == k:
            return curr.val
        curr = curr.right
```

This uses an **iterative** inorder traversal with an explicit stack
(instead of recursion), and returns **as soon as** the k-th node is
popped — no need to visit the rest of the tree. This is still O(n) in the
absolute worst case (`k` = total node count), but for small `k` on a large
tree, it does dramatically less work in practice, and avoids building the
full `result` list. Space also improves to O(h) instead of O(n), since the
stack only ever holds one root-to-leaf path at a time, not every value in
the tree.

## An O(1)-Space Alternative: Morris Traversal

The early-stopping version above already improves space from O(n) to
O(h) (tree height) by using an explicit stack instead of building a full
list. **Morris Traversal** goes one step further: true **O(1)** extra
space, no stack and no recursion at all.

### Intuition

Both the recursive and stack-based versions need extra memory to
"remember where to come back to" after finishing a left subtree — that's
literally what the call stack / explicit stack stores. Morris Traversal
eliminates that need by **temporarily borrowing empty pointers already in
the tree** to record that information instead.

Specifically: every node that has a left subtree also has an **inorder
predecessor** — the rightmost node in that left subtree (the node that
should be visited immediately before the current one, in sorted order).
That predecessor's `.right` pointer is _always_ empty at the point you'd
want to use it (since it's the rightmost node in the subtree). Morris
Traversal temporarily repurposes that empty pointer as a "thread" pointing
back to the current node — effectively building a temporary shortcut back
"up" the tree, standing in for what a call stack would normally remember.

### The Two Cases at Each Node

- **No left child** → there's nothing to explore first, so visit this
  node immediately (decrement `k`), then move right.
- **Has a left child** → find the predecessor (rightmost node in the left
  subtree):
  - **Predecessor's `.right` is empty** → no thread exists yet. Create
    one (`pred.right = curr`), then move into the left subtree
    (`curr = curr.left`). This is like "pushing" onto an implicit stack,
    but using the tree's own structure instead of real memory.
  - **Predecessor's `.right` already points back to `curr`** → we've
    already fully explored the left subtree and looped back via the
    thread. Remove it (`pred.right = None`, restoring the tree to its
    original shape), visit the current node (decrement `k`), then move
    right.

### The Code

```python
def kthSmallest(self, root, k):
    curr = root

    while curr:
        if not curr.left:
            k -= 1
            if k == 0:
                return curr.val
            curr = curr.right
        else:
            pred = curr.left
            while pred.right and pred.right != curr:
                pred = pred.right

            if not pred.right:
                pred.right = curr
                curr = curr.left
            else:
                pred.right = None
                k -= 1
                if k == 0:
                    return curr.val
                curr = curr.right

    return -1
```

- The `while pred.right and pred.right != curr` loop walks right from
  `curr.left` to find the predecessor — stopping either when it hits a
  dead end (`pred.right` is `None`, first visit) or hits the thread back
  to `curr` (second visit, meaning the left subtree is done).
- Each node is visited (and `k` decremented) at the exact same logical
  point an inorder traversal would visit it — Morris Traversal doesn't
  change _when_ nodes are visited, only _how_ the "return address" is
  remembered.
- **The tree is fully restored** to its original shape by the time the
  traversal finishes — every thread that's created is also removed before
  the algorithm moves on, so this is non-destructive despite temporarily
  mutating `.right` pointers mid-traversal.

### Complexity

- **Time: O(n)** — this looks like it might be worse than O(n) because of
  the extra predecessor-finding walk, but each edge in the tree is
  traversed at most twice (once to create the thread, once to remove it),
  so the total work stays linear.
- **Space: O(1)** — no stack, no recursion, only a couple of pointer
  variables (`curr`, `pred`). This is the theoretical best possible space
  complexity for this problem.

### Why Bother, If the Stack Version Is Already O(h)?

For a balanced BST, O(h) is already O(log n), so the practical difference
is small. But for a **degenerate (linked-list-shaped) BST**, `h` can be
`O(n)` — at which point the stack version's space usage degrades to O(n)
too, while Morris Traversal stays at true O(1) regardless of tree shape.
It's also a favorite interview "can you do better?" follow-up precisely
because it's non-obvious and demonstrates a deeper understanding of tree
structure manipulation.

## Pattern to Remember

**"Do I need values from a BST in sorted order?" → inorder traversal,
which produces sorted order automatically, with no separate sort step.**

This is the master key for a whole category of BST problems:

- Kth Smallest Element in a BST (this problem)
- Validate Binary Search Tree — check that an inorder traversal is
  strictly increasing
- Convert BST to Sorted Doubly Linked List — inorder traversal while
  relinking pointers instead of collecting into a list
- Minimum Absolute Difference in BST — inorder traversal, comparing each
  value to the previous one as you go
- Binary Tree Inorder Traversal — Morris Traversal itself is the direct
  O(1)-space answer to "traverse this tree without recursion or a stack"

## Edge Cases Handled

- **Single-node tree** (`[1]`, `k=1`) — traversal visits just the root,
  `result = [1]`, `result[0] = 1`. Correct.
- **`k` equal to total node count** — verified via the second test case
  (`k=3` on a 6-node tree) — returns the median-ish value correctly since
  the full sorted list is available.
- **Left-skewed / right-skewed trees** — inorder traversal handles these
  the same as any other shape; no special casing needed, since the
  algorithm doesn't assume balance.

## What I Got Wrong / Things to Watch

_(fill in anything that tripped you up — e.g. did you consider the
early-stopping iterative version, or go straight for the simpler
build-then-index approach? Worth noting which one you'd reach for first in
an interview under time pressure.)_
