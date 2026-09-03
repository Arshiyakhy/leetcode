# 141. Linked List Cycle

**Link:** https://leetcode.com/problems/linked-list-cycle/
**Difficulty:** Easy
**Topic:** Linked List, Two Pointers (Floyd's Cycle Detection)

## Problem

Given the `head` of a linked list, determine if the list has a cycle in
it — i.e., some node's `.next` pointer eventually loops back to a node
earlier in the list, instead of ending at `None`.

```
Input:  3 -> 2 -> 0 -> -4 -> (back to node with value 2)
Output: true
```

## The Brute Force (and why we don't stop there)

The natural first idea: remember every node you've visited, and if you
ever land on a node you've already seen, there's a cycle.

```python
seen = set()
node = head
while node:
    if node in seen:
        return True
    seen.add(node)
    node = node.next
return False
```

This works and is **O(n) time**, but it costs **O(n) space** — in the
worst case (no cycle), you store every single node in the set before
concluding `False`. For a problem this fundamental, there's a way to get
the same O(n) time _without_ any extra memory.

## The Key Insight

Imagine two runners on a track: one **slow** (moves 1 step at a time) and
one **fast** (moves 2 steps at a time). Two possibilities:

- **If the list has no cycle:** the fast runner reaches the end (`None`)
  first and the race simply terminates — no way for them to ever meet.
- **If the list has a cycle:** both runners eventually enter the loop.
  Once they're both inside the same finite loop, the fast runner is
  gaining on the slow one by exactly 1 step every iteration (fast moves 2,
  slow moves 1 — net gap closes by 1 each time). Since the loop is finite,
  the fast runner is **guaranteed** to eventually lap the slow one and
  land on the exact same node.

So instead of remembering every node (brute force), you only need to ask:
**do these two pointers, moving at different speeds, ever collide?** No
extra memory needed — just two pointers and a comparison.

This is why it's called **Floyd's Cycle Detection**, or informally
"tortoise and hare."

## Walkthrough of the Code

```python
slow, fast = head, head
while fast and fast.next:
    slow = slow.next
    fast = fast.next.next
    if slow == fast:
        return True
return False
```

- Both pointers start at `head`.
- **Loop condition — `while fast and fast.next`:** this checks fast can
  safely take its next 2-step move. If `fast` is `None` (reached the end)
  or `fast.next` is `None` (one more step would overshoot into nothing),
  there's no cycle — the list simply ended.
- **Each iteration:**
  - `slow` advances **1** node.
  - `fast` advances **2** nodes (`fast.next.next`).
  - **Check for collision** — if `slow is fast` (comparing node identity,
    not value), the fast pointer has lapped the slow one, which can only
    happen inside a cycle. Return `True`.
- If the loop exits naturally (fast ran off the end), there's no cycle —
  return `False`.

### Trace through a cycle: `3 -> 2 -> 0 -> -4 -> (back to 2)`

| step  | slow | fast | slow == fast?           |
| ----- | ---- | ---- | ----------------------- |
| start | 3    | 3    | — (loop hasn't run yet) |
| 1     | 2    | 0    | No                      |
| 2     | 0    | 2    | No                      |
| 3     | -4   | -4   | **Yes** → return `True` |

The fast pointer wrapped around the cycle and caught up to the slow one.

### Trace through no cycle: `1 -> 2 -> None`

| step  | slow | fast | condition check                     |
| ----- | ---- | ---- | ----------------------------------- |
| start | 1    | 1    | fast and fast.next → True, continue |
| 1     | 2    | None | fast is None → loop exits           |

Return `False` — correct, no cycle exists.

## Complexity

- **Time: O(n)** — even in the cycle case, the fast pointer can lap the
  slow one at most once around the length of the cycle, so total steps
  stay linear in the number of nodes.
- **Space: O(1)** — only two pointer variables, regardless of list length.
  This is the entire reason Floyd's algorithm is preferred over the
  hash-set approach: same time complexity, but no extra memory.

## Pattern to Remember

**"Detect a cycle / find a midpoint / detect a loop" → two pointers moving
at different speeds (slow = 1 step, fast = 2 steps).**

This exact fast/slow pointer setup is the foundation for a family of
linked list problems:

- Linked List Cycle (this problem) — does a cycle exist?
- Linked List Cycle II — find _where_ the cycle begins (extension of this
  same technique, with an extra phase after detection)
- Middle of the Linked List — when fast reaches the end, slow is
  guaranteed to be at the midpoint
- Palindrome Linked List — find the midpoint (via fast/slow), then reverse
  the second half and compare

## Edge Cases Handled

- **Empty list** (`head = None`) — the `while fast and fast.next` check
  fails immediately (`fast` is `None`), loop never runs, returns `False`.
- **Single node, no cycle** (`[1]`) — `fast.next` is `None` right away,
  loop never runs, returns `False`.
- **Single node with self-cycle** (node points to itself) — `slow` and
  `fast` would both immediately point to the same node on the first
  iteration, correctly returning `True`.
- **Comparing node identity, not value** — the check `slow == fast`
  compares the actual node objects (identity), which matters because two
  _different_ nodes could coincidentally hold the same `val` — only
  reference equality proves the pointers have actually converged on the
  same node.

## What I Got Wrong / Things to Watch

_(fill in anything that tripped you up — e.g. did you initially forget the
`fast.next` half of the loop condition and hit an `AttributeError` trying
to call `.next.next` on `None`?)_
