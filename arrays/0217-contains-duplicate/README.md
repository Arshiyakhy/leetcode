# 217. Contains Duplicate

**Link:** https://leetcode.com/problems/contains-duplicate/
**Difficulty:** Easy
**Topic:** Array, Hash Set

## Problem

Given an integer array `nums`, return `true` if any value appears **at
least twice** in the array, and `false` if every element is distinct.

```
Input:  nums = [1, 2, 3, 1]
Output: true        # 1 appears at index 0 and index 3
```

## The Brute Force (and why we don't stop there)

The obvious idea: compare every pair of elements.

```python
for i in range(len(nums)):
    for j in range(i + 1, len(nums)):
        if nums[i] == nums[j]:
            return True
return False
```

That's **O(n²)** — for every element, we rescan the rest of the array to
check for a match. There's also a common "clever" alternative:

```python
return len(nums) != len(set(nums))
```

This is O(n) time and correct, but it always builds the _entire_ set before
checking anything — even if a duplicate shows up on the very first two
elements. It also throws away useful information: it tells you duplicates
exist somewhere, but you get no early exit and no positional info if you
needed it. Your solution fixes both of these.

## The Key Insight

Just like Two Sum, this is another "**have I seen this before?**" problem —
which is the signal for a hash-based structure instead of nested loops or
re-scanning.

The difference from Two Sum is what you need to remember about "before":
Two Sum needed to know _where_ (the index) you saw a number, because it had
to return positions. Here, you only need to know _whether_ you've seen a
number at all — no index required. That's exactly what a **set** is for: a
hash map without the value, just fast O(1) membership testing.

## Walkthrough of the Code

```python
s = set()
for n in nums:
    if n in s:
        return True
    s.add(n)
return False
```

- `s` is a hash set of every number seen so far.
- For each number `n`:
  1. **Check first** — if `n` is already in `s`, we've found a duplicate.
     Return `True` immediately — no need to keep scanning.
  2. **Then add** — if it wasn't a duplicate, record it in `s` so future
     elements can check against it.
- If we make it through the whole array without ever finding a match,
  every element was unique — return `False`.

### Trace through `[1, 2, 3, 1]`

| n   | n in s? | action        | s after     |
| --- | ------- | ------------- | ----------- |
| 1   | No      | add           | `{1}`       |
| 2   | No      | add           | `{1, 2}`    |
| 3   | No      | add           | `{1, 2, 3}` |
| 1   | **Yes** | return `True` | —           |

Notice we stop at the 4th element instead of finishing the full pass — this
is the early-exit advantage over `len(nums) != len(set(nums))`, which would
have built the full set (`{1, 2, 3}`, size 3) and _then_ compared lengths.
Same time complexity on paper, but your version does less work on average
and exits as soon as it can prove the answer.

## Complexity

- **Time: O(n)** — single pass in the worst case (no duplicates); early
  exit as soon as one is found.
- **Space: O(n)** — worst case (no duplicates at all), the set grows to
  hold every element.

Same trade-off shape as Two Sum: O(n) space bought to bring time down from
O(n²) to O(n).

## Pattern to Remember

**"Have I seen this before?" → hash set (if you only need yes/no), hash
map (if you need to remember _where_ or _what else_ about it).**

This is the same family as Two Sum, just simpler — you dropped the "index"
requirement, so the map became a set. Recognizing _which_ of these two you
need (set vs. map) usually comes down to one question: _do I need to
recall anything besides "was it there"?_ If yes → map. If no → set.

Related problems that reuse this exact pattern:

- Contains Duplicate (this problem) — set, yes/no
- Two Sum — map, need the index too
- Contains Duplicate II (values within `k` distance) — map, need to compare
  indices
- Longest Consecutive Sequence — set, used to skip re-counting streaks

## Edge Cases Handled

- **Empty array** (`[]`) — loop never runs, falls through to `return
False` correctly.
- **Single element** — no duplicate possible, correctly returns `False`.
- **All identical elements** (`[2, 2, 2]`) — catches the duplicate on the
  second element, returns `True` immediately without scanning the rest.

## What I Got Wrong / Things to Watch

_(fill in anything that tripped you up here)_
