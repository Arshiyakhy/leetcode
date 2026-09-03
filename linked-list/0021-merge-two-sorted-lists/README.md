# 21. Merge Two Sorted Lists

**Link:** https://leetcode.com/problems/merge-two-sorted-lists/
**Difficulty:** Easy
**Topic:** Linked List, Recursion, Two Pointers

## Problem

Given the heads of two **sorted** linked lists `list1` and `list2`, merge
them into one sorted list by splicing together the existing nodes (not
creating new ones), and return the head of the merged list.

```
Input:  list1 = 1 -> 2 -> 4,  list2 = 1 -> 3 -> 4
Output: 1 -> 1 -> 2 -> 3 -> 4 -> 4
```

## The Key Insight

Both lists are already sorted — that's the constraint that makes this
efficient. This is the exact same idea behind the "merge" step of merge
sort: **since both lists are individually sorted, you only ever need to
compare the two current front elements to know which one belongs next.**
You never need to look further ahead or backtrack.

That gives a clean **recursive definition**:

> The merged list starting from `list1` and `list2` is: take whichever
> head is smaller, and attach it to the front of "the merge of everything
> else" (the recursive result of merging the rest of that list with the
> other list untouched).

This is a classic case of a problem having **optimal substructure** —
merging the full lists reduces directly to solving the same problem on a
smaller pair of lists.

## Walkthrough of the Code

```python
if list1 is None:
    return list2
if list2 is None:
    return list1

if list1.val <= list2.val:
    list1.next = self.mergeTwoLists(list1.next, list2)
    return list1
else:
    list2.next = self.mergeTwoLists(list1, list2.next)
    return list2
```

- **Base cases:** if either list has run out (`None`), the answer is
  simply _the other list_ — there's nothing left to compare, so whatever
  remains of the non-empty list is already sorted and can be attached
  as-is.
- **Recursive case:** compare the two current heads.
  - If `list1.val <= list2.val` (using `<=`, not `<`, so ties keep
    `list1`'s node first — this also matters for stability with equal
    values):
    - `list1` should come first in the result.
    - Recursively merge `list1.next` with the _untouched_ `list2`, and
      attach that result as `list1.next` — this correctly splices in
      "the merge of everything remaining."
    - Return `list1` as the head of this sub-merge.
  - Otherwise (mirror case), do the same with `list2` in front.
- **No new nodes are created** — the function only ever rewires existing
  `.next` pointers (`list1.next = ...`), exactly as the problem requires
  ("splicing together the existing nodes").

### Trace through `list1 = [1, 2, 4]`, `list2 = [1, 3, 4]`

| call                    | list1.val | list2.val | comparison                   | result of this call       |
| ----------------------- | --------- | --------- | ---------------------------- | ------------------------- |
| merge([1,2,4], [1,3,4]) | 1         | 1         | 1 <= 1 → take list1          | 1 -> merge([2,4],[1,3,4]) |
| merge([2,4], [1,3,4])   | 2         | 1         | 2 > 1 → take list2           | 1 -> merge([2,4],[3,4])   |
| merge([2,4], [3,4])     | 2         | 3         | 2 <= 3 → take list1          | 2 -> merge([4],[3,4])     |
| merge([4], [3,4])       | 4         | 3         | 4 > 3 → take list2           | 3 -> merge([4],[4])       |
| merge([4], [4])         | 4         | 4         | 4 <= 4 → take list1          | 4 -> merge([],[4])        |
| merge([], [4])          | —         | —         | list1 is None → return list2 | 4                         |

Unwinding the recursion: `1 -> 1 -> 2 -> 3 -> 4 -> 4` ✓

## Complexity

- **Time: O(m + n)** — where `m` and `n` are the lengths of `list1` and
  `list2`. Every recursive call consumes exactly one node from one of the
  two lists, and the recursion ends once both are exhausted — so the total
  number of calls is bounded by `m + n`.
- **Space: O(m + n)** — this is the trade-off worth knowing. Each
  recursive call adds a frame to the call stack, and the recursion depth
  equals the total number of nodes processed. An **iterative** version
  (using a dummy head and a `tail` pointer, looping instead of recursing)
  achieves the same O(m + n) time in **O(1)** space, since it avoids the
  call stack entirely. For very long lists, the iterative version is
  safer (no risk of hitting Python's recursion limit / stack overflow) —
  worth having both in your back pocket.

## Pattern to Remember

**"Merge two already-sorted sequences" → compare fronts, take the smaller,
recurse (or loop) on what's left.**

This exact merge step is the beating heart of **merge sort** — this
problem is literally "implement the merge step of merge sort, but on
linked lists instead of arrays." Recognizing that connection is useful:
any time you're asked to combine two sorted structures into one sorted
structure, this comparison-and-splice logic is the answer.

Related problems building on this:

- Merge Two Sorted Lists (this problem)
- Merge k Sorted Lists — repeatedly apply this same pairwise merge (or use
  a heap) across more than two lists
- Sort List — full merge sort on a linked list, using this exact merge
  step as its combine phase

## Edge Cases Handled

- **Both lists empty** (`[]`, `[]`) — first base case (`list1 is None`)
  triggers immediately, returns `list2` (which is also `None`). Correct.
- **One list empty** (`[]`, `[0]`) — `list1 is None` triggers, returns
  `list2` as-is. Correct — nothing to merge, the non-empty list is
  already the answer.
- **Equal values across lists** (both heads = `4` in the trace above) —
  handled correctly by using `<=` rather than `<`, so ties resolve
  deterministically (list1's node goes first) instead of being ambiguous.

## What I Got Wrong / Things to Watch

_(fill in anything that tripped you up — e.g. did you use `<` instead of
`<=` initially and get bitten by duplicate values? Did you consider the
iterative version and decide against it?)_
