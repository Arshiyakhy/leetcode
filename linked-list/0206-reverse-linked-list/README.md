# 206. Reverse Linked List

**Link:** https://leetcode.com/problems/reverse-linked-list/
**Difficulty:** Easy
**Topic:** Linked List, Two Pointers

## Problem

Given the `head` of a singly linked list, reverse the list and return the
new head.

```
Input:  1 -> 2 -> 3 -> 4 -> 5 -> None
Output: 5 -> 4 -> 3 -> 2 -> 1 -> None
```

## Why This Isn't Like Array Problems

With an array, "reversing" is just re-indexing — you can jump straight to
`nums[len(nums)-1-i]`. A linked list has **no random access**: the only way
to get from one node to another is by following `.next` pointers, and
those pointers only go one direction (forward). To reverse the list, you
have to physically flip every `.next` pointer to point backward instead of
forward — you can't just "read it backward."

That's the whole challenge here: how do you flip every arrow without
losing your place in the list, given that once you overwrite `curr.next`,
you've destroyed your only way to reach the rest of the list?

## The Key Insight

The fix is to **save the "next" pointer before you overwrite it.** At each
node, you need to juggle three things at once:

1. **temp** — where you were _about_ to go (save this before it's gone)
2. **curr.next** — flip it to point backward, at `prev`
3. **prev, curr** — both slide forward one step, using the saved `temp`

This is a **two-pointer** technique (`prev` and `curr`), walking forward in
lockstep while reversing the arrow behind them as they go — like flipping
dominoes over one at a time as you walk past them, without losing track of
the next domino in line.

## Walkthrough of the Code

```python
prev, curr = None, head

while curr:
    temp = curr.next
    curr.next = prev
    prev = curr
    curr = temp
return prev
```

- **Initial state:** `prev = None` (there's nothing before the first
  node — its `.next` should eventually point to `None`, marking the new
  tail). `curr = head` (start at the front of the original list).
- **Inside the loop, at each node**, in this exact order:
  1. `temp = curr.next` — **save** the next node before we lose access to
     it (this is the critical step — skip it and the rest of the list is
     gone).
  2. `curr.next = prev` — **flip the arrow**: this node now points
     backward to whatever came before it.
  3. `prev = curr` — **advance prev** to the node we just finished
     flipping.
  4. `curr = temp` — **advance curr** to the node we saved in step 1.
- **Loop ends** when `curr` becomes `None` (we've walked off the end of
  the original list).
- **Return `prev`** — at that point, `prev` is sitting on the _last_ node
  of the original list, which is now the _first_ node of the reversed
  list — exactly the new head we need.

### Trace through `1 -> 2 -> 3 -> None`

| step  | prev | curr | temp (curr.next, saved) | curr.next set to |
| ----- | ---- | ---- | ----------------------- | ---------------- |
| start | None | 1    | —                       | —                |
| 1     | 1    | 2    | 2                       | 1.next = None    |
| 2     | 2    | 3    | 3                       | 2.next = 1       |
| 3     | 3    | None | None                    | 3.next = 2       |

Loop ends (`curr` is `None`). Return `prev = 3`.

Resulting list: `3 -> 2 -> 1 -> None` ✓

## Complexity

- **Time: O(n)** — visit each node exactly once, constant work per node.
- **Space: O(1)** — only three pointer variables (`prev`, `curr`, `temp`),
  no matter how long the list is. This beats a recursive solution, which
  would use **O(n)** space for the call stack (one stack frame per node) —
  worth knowing both, but the iterative version is the one to default to
  for a long list, to avoid stack overflow.

## Pattern to Remember

**"Reversing pointers in a linked list" → two pointers (`prev`, `curr`)
walking forward together, with a `temp` variable to preserve the link
you're about to destroy.**

This exact three-pointer dance (save next → flip → advance both) is the
foundation for a huge family of linked list problems:

- Reverse Linked List (this problem) — reverse the whole list
- Reverse Linked List II — reverse only a sub-section between positions
  `left` and `right`
- Swap Nodes in Pairs — reverse two nodes at a time
- Reverse Nodes in k-Group — reverse in chunks of `k`

The core habit worth internalizing: **whenever you're about to overwrite a
`.next` pointer, ask "do I still need the old value of this?" — if yes,
save it in a temp variable first.**

## Edge Cases Handled

- **Empty list** (`head = None`) — the `while curr` loop never executes
  (since `curr` starts as `None`), and `prev` (still `None`) is returned
  correctly.
- **Single node** (`[5]`) — loop runs once: `temp = None`, `curr.next =
None` (already correct, since it was already the tail), `prev` becomes
  that node, `curr` becomes `None`, loop ends. Returns the same single
  node — correct, since reversing a 1-element list is a no-op.
- **Two nodes** — traced conceptually the same as the 3-node example
  above; verified working via the `[1, 2]` test case.

## What I Got Wrong / Things to Watch

_(fill in anything that tripped you up — e.g. did you first forget to save
`temp` before reassigning `curr.next`, losing the rest of the list? That's
the single most common bug on this problem.)_
