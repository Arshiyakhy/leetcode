# 143. Reorder List

**Link:** https://leetcode.com/problems/reorder-list/
**Difficulty:** Medium
**Topic:** Linked List, Two Pointers, Recursion (combines: midpoint finding + reversal + merge)

## Problem

Given the head of a singly linked list `L0 -> L1 -> ... -> Ln`, reorder it
**in-place** into the form:

```
L0 -> Ln -> L1 -> Ln-1 -> L2 -> Ln-2 -> ...
```

You may not change the node values — only rewire `.next` pointers. No
value is returned; the list is modified in place.

```
Input:  1 -> 2 -> 3 -> 4
Output: 1 -> 4 -> 2 -> 3
```

## The Brute Force (and why we don't stop there)

The direct-but-clumsy idea: dump every node into an array (or use a
stack), then rebuild the list by alternately picking from the front and
back of that array.

```python
nodes = []
node = head
while node:
    nodes.append(node)
    node = node.next

i, j = 0, len(nodes) - 1
while i < j:
    nodes[i].next = nodes[j]
    i += 1
    if i == j:
        break
    nodes[j].next = nodes[i]
    j -= 1
nodes[i].next = None
```

This is **O(n) time** but **O(n) space** — you're storing a reference to
every single node in an array just to get random access to "the node from
the end." The whole point of the smarter solution is: linked lists don't
support random access, but you can _simulate_ "access from both ends" in
O(1) space by physically splitting and reversing the list instead.

## The Key Insight

Reordering `L0, Ln, L1, Ln-1, L2, Ln-2, ...` is really just **interleaving
two halves of the list — the front half in its original order, and the
back half in reverse order.**

Break the problem into three sub-problems you've already solved
individually:

1. **Find the middle** of the list → _fast/slow pointer_ technique (same
   idea as Linked List Cycle / Middle of the Linked List).
2. **Reverse the second half** → the exact three-pointer reversal from
   Reverse Linked List.
3. **Merge the two halves, alternating nodes** → the same splicing logic
   as Merge Two Sorted Lists, just alternating strictly instead of
   comparing values.

Recognizing that a "new" problem is actually three familiar patterns
chained together is a big part of getting efficient at these — the hard
part isn't inventing new tricks, it's noticing which old tricks combine.

## Walkthrough of the Code

### Step 1 — Find the middle

```python
slow, fast = head, head.next
while fast and fast.next:
    slow = slow.next
    fast = fast.next.next
```

Note `fast` starts at `head.next` (not `head`) here — this is a deliberate
choice so that for even-length lists, `slow` lands on the **first** node
of the second half's "attachment point" rather than splitting evenly down
the middle. This specific offset is what makes the merge step come out
correctly later (verify with the trace below).

### Step 2 — Reverse the second half

```python
second = slow.next
prev = slow.next = None
while second:
    tmp = second.next
    second.next = prev
    prev = second
    second = tmp
```

- `second` becomes the head of the back half (everything after `slow`).
- `slow.next` is cut to `None` — this **splits the list into two
  independent halves**; without this, the first half would still be
  linked into the reversal process.
- The `while second` loop is the identical reversal logic from Reverse
  Linked List. After this, `prev` is the head of the _reversed_ second
  half.

### Step 3 — Merge, alternating

```python
first, second = head, prev
while second:
    tmp1, tmp2 = first.next, second.next
    first.next = second
    second.next = tmp1
    first, second = tmp1, tmp2
```

- `first` walks the original front half; `second` walks the reversed back
  half.
- At each step: save both `.next` pointers first (since we're about to
  overwrite them), then splice `second` in right after `first`, then
  `second.next` points to what used to be `first.next` (continuing the
  front half).
- Advance both pointers to their saved "next" values and repeat.
- **Loop ends when `second` is `None`** — this naturally happens once the
  (shorter or equal) reversed back half is exhausted, which correctly
  leaves any leftover middle node from an odd-length list in place at the
  end untouched.

### Trace through `[1, 2, 3, 4]`

**Step 1 (find middle):** `fast` starts at `2`.

- iter 1: `slow = 2`, `fast = 4`. Loop condition (`fast.next` = `None`)
  fails, stop.
- `slow` = node `2`.

**Step 2 (reverse second half):** `second = slow.next = 3`, cut `slow.next
= None` (list is now `1 -> 2` and `3 -> 4` separately).

- Reversing `3 -> 4` gives `4 -> 3` (`prev` ends at node `4`).

**Step 3 (merge):** `first = 1` (head of `1 -> 2`), `second = 4` (head of
`4 -> 3`).

- iter 1: `tmp1=2, tmp2=3`. `1.next = 4`, `4.next = 2`. Now `first=2,
second=3`.
- iter 2: `tmp1=None, tmp2=None`. `2.next = 3`, `3.next = None`. Now
  `first=None, second=None`.
- Loop ends (`second` is `None`).

Result: `1 -> 4 -> 2 -> 3` ✓ — exactly matches the expected output.

## Complexity

- **Time: O(n)** — each of the three steps (find middle, reverse, merge)
  is an independent O(n) pass; O(n) + O(n) + O(n) is still O(n) overall.
- **Space: O(1)** — only a handful of pointer variables throughout; no
  arrays, no recursion, no extra data structures. This is the best
  possible space complexity, beating the O(n)-space array approach.

## Pattern to Remember

**Complex in-place linked list restructuring often decomposes into: find
midpoint (fast/slow) → reverse a portion (three-pointer reversal) → merge
back together (splice while walking two pointers).**

This exact three-step combo pattern reappears in:

- Reorder List (this problem)
- Palindrome Linked List — find midpoint, reverse second half, then
  _compare_ instead of merge
- Odd Even Linked List — a related but simpler splicing pattern (no
  reversal needed)

Once you've internalized the three individual sub-patterns (midpoint,
reversal, merge/splice) from earlier problems, recognizing when a new
problem is "just" a combination of them becomes much faster than solving
from scratch each time.

## Edge Cases Handled

- **Single node** (`[1]`) — `fast = head.next = None` immediately, loop
  never runs, `slow` stays at the only node. `second = slow.next = None`,
  so the reversal loop never runs (`prev` stays `None`). Merge loop
  condition (`while second`) is immediately `False` since `second = prev =
None`. List is untouched — correct, nothing to reorder.
- **Two nodes** (`[1, 2]`) — verified via test case, list stays as `1 ->
2` (already in the required order for n=1).
- **Even vs. odd length** — the `fast = head.next` starting offset (rather
  than `fast = head`) specifically ensures the split point works out
  correctly for both cases; verified with both the 4-node and 5-node test
  cases above.

## What I Got Wrong / Things to Watch

_(fill in anything that tripped you up — e.g. did the fast pointer's
starting position confuse you at first? Did you originally try the O(n)
space array approach before working out the O(1) in-place version?)_
