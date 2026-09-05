# 19. Remove Nth Node From End of List

**Link:** https://leetcode.com/problems/remove-nth-node-from-end-of-list/
**Difficulty:** Medium
**Topic:** Linked List, Two Pointers

## Problem

Given the `head` of a linked list, remove the `n`-th node **from the
end**, and return the head of the resulting list.

```
Input:  head = [1, 2, 3, 4, 5], n = 2
Output: [1, 2, 3, 5]      # the 2nd node from the end (value 4) is removed
```

## Why This Is Trickier Than It Looks

A singly linked list only lets you walk **forward**. "The n-th node from
the end" is naturally a _backward_-counting concept — but you can't walk
backward. The whole problem is: how do you find a position defined
relative to the end, in a structure that only lets you move toward the
end?

## Your Approach: Two Passes

Your solution resolves this with the most direct fix: **since you can't
count from the end directly, first find out how long the list is, then
convert "n-th from the end" into "n-th from the start."**

```python
N = 0
cur = head
while cur:
    N += 1
    cur = cur.next

removeIndex = N - n
if removeIndex == 0:
    return head.next

cur = head
for i in range(N - 1):
    if (i + 1) == removeIndex:
        cur.next = cur.next.next
        break
    cur = cur.next
return head
```

### Walkthrough

- **Pass 1 — count the length:** walk the whole list once, incrementing
  `N`. After this, `N` is the total number of nodes.
- **Convert the position:** `removeIndex = N - n` is the **0-indexed
  position from the start** of the node to remove. (E.g., 5 nodes,
  removing the 2nd from the end → `5 - 2 = 3`, i.e., index 3, which is the
  4th node — matches the example.)
- **Special case — removing the head:** if `removeIndex == 0`, the node to
  remove _is_ the head itself. You can't "skip to before it and unlink it"
  the normal way (there's no node before the head), so this is handled
  separately: just return `head.next` directly.
- **Pass 2 — walk to just before the target, then unlink:** starting again
  from `head`, walk forward. The loop looks for the position **one before**
  `removeIndex` (checking `(i + 1) == removeIndex`) — because to remove a
  node, you need a handle on the node _before_ it, so you can do
  `cur.next = cur.next.next` (skip over the target node entirely).

### Trace through `[1, 2, 3, 4, 5]`, `n = 2`

**Pass 1:** count nodes → `N = 5`.

**Convert:** `removeIndex = 5 - 2 = 3` (0-indexed: node `4` is at index 3).

**Pass 2:** walk from `head`, looking for `i+1 == 3`, i.e. `i == 2`:

| i   | cur (before check) | (i+1) == 3?                                                       |
| --- | ------------------ | ----------------------------------------------------------------- |
| 0   | 1                  | 1 == 3? No                                                        |
| 1   | 2                  | 2 == 3? No                                                        |
| 2   | 3                  | 3 == 3? **Yes** → `cur.next = cur.next.next` (skip node 4), break |

`cur` was sitting on node `3` when the match hit, so `3.next` gets set to
`5` (skipping `4` entirely). Result: `1 -> 2 -> 3 -> 5` ✓

## Complexity

- **Time: O(n)** — two full passes over the list (or fewer, since pass 2
  can `break` early), but two passes is still O(n) + O(n) = O(n) overall.
- **Space: O(1)** — only a few counter/pointer variables.

## A One-Pass Alternative (worth knowing)

Since this problem is a common interview follow-up ("can you do it in one
pass?"), here's the standard trick: use **two pointers with a gap of `n`
between them**, plus a dummy node to sidestep the "removing the head"
special case entirely.

```python
dummy = ListNode(0, head)
left = dummy
right = head

# Advance `right` n steps ahead first, opening a gap of n
for _ in range(n):
    right = right.next

# Move both pointers together until `right` falls off the end;
# at that point `left` is sitting just before the node to remove
while right:
    left = left.next
    right = right.next

left.next = left.next.next
return dummy.next
```

The idea: if `right` is always exactly `n` nodes ahead of `left`, then the
moment `right` reaches the end (`None`), `left` must be sitting exactly
`n` nodes from the end — i.e., right before the node to remove. This finds
the target in a **single pass**, and the `dummy` node means removing the
real head requires no special-casing (since `dummy` always exists "before"
the head).

This is O(n) time (same as your version, since one pass here is no faster
asymptotically than your two passes — both are O(n)), but it does it in a
single traversal, and the dummy-node trick is broadly useful across linked
list problems.

## Pattern to Remember

**"Find a node whose position is defined relative to the end / relative to
another node" → either (a) two passes: measure the whole structure first,
then compute an absolute position, or (b) two pointers with a fixed gap,
moved together — one pass.**

Both are valid and O(n) — (a) is often more intuitive to write correctly
under pressure, (b) is the "expected" optimization interviewers may probe
for.

Related problems:

- Remove Nth Node From End of List (this problem)
- Middle of the Linked List — a simpler cousin of the two-pointer-gap idea
  (gap doesn't even need computing — just move fast at 2x speed)
- Linked List Cycle — different problem, same "two pointers moving through
  a list at a relative offset" family

## Edge Cases Handled

- **Removing the head** (`[1, 2]`, `n = 2`) — the `removeIndex == 0`
  branch catches this and returns `head.next` directly, avoiding the
  "no node before the head to unlink from" problem.
- **Single-node list, remove it** (`[1]`, `n = 1`) — `N = 1`,
  `removeIndex = 0`, hits the head-removal branch, returns `head.next =
None`. Correct — result is an empty list.
- **`n` equals list length exactly** — same as the head-removal case
  above, since removing the n-th-from-end when n = length means removing
  the very first node.

## What I Got Wrong / Things to Watch

_(fill in anything that tripped you up — e.g. did you initially forget the
`removeIndex == 0` special case and get an error trying to unlink "before"
the head? Did the off-by-one in converting `N - n` to a 0-indexed position
take a couple tries to get right?)_
