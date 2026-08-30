# 1. Two Sum

**Link:** https://leetcode.com/problems/two-sum/
**Difficulty:** Easy
**Topic:** Array, Hash Map

## Problem

Given an array of integers `nums` and an integer `target`, return the indices
of the two numbers that add up to `target`. Each input has exactly one
solution, and you cannot use the same element twice.

```
Input:  nums = [2, 7, 11, 15], target = 9
Output: [0, 1]        # nums[0] + nums[1] == 9
```

## The Brute Force (and why we don't stop there)

The obvious first idea: check every pair of numbers.

```python
for i in range(len(nums)):
    for j in range(i + 1, len(nums)):
        if nums[i] + nums[j] == target:
            return [i, j]
```

This works, but for every element you scan the rest of the array looking for
its complement. That's **O(n²)** time — for `n = 10,000` that's up to 100
million comparisons. We can do way better by trading a bit of space for
speed.

## The Key Insight

At every index `i`, there's really only one question that matters:

> "Have I already seen the number that, combined with `nums[i]`, gives me `target`?"

That number is `target - nums[i]` — call it the **complement**. If we've
seen the complement before, we're done. If not, we log the current number so
future elements can check against it.

The brute force re-derives "have I seen X?" by re-scanning the array every
time. A **hash map** answers "have I seen X?" in O(1), because hashing gives
you near-instant lookup instead of a linear scan. That's the whole trick:
replace repeated searching with a single lookup table.

## Walkthrough of the Code

```python
seen = {}
for i, num in enumerate(nums):
    remaining = target - num
    if remaining in seen:
        return [seen[remaining], i]
    seen[num] = i
```

- `seen` is a hash map of `{number: index}` — every number we've passed so
  far, and where we saw it.
- On each iteration, compute `remaining = target - num`. This is "the number
  I need to complete the pair."
- **Check before you insert.** If `remaining` is already a key in `seen`,
  we've found our pair — return the earlier index (`seen[remaining]`) and
  the current index (`i`).
- If not found, add the current number to `seen` and move on.

### Trace through `[2, 7, 11, 15]`, `target = 9`

| i   | num | remaining (9 - num) | remaining in seen?        | seen after this step |
| --- | --- | ------------------- | ------------------------- | -------------------- |
| 0   | 2   | 7                   | No                        | `{2: 0}`             |
| 1   | 7   | 2                   | **Yes** → return `[0, 1]` | —                    |

We never even reach index 2 or 3 — we stop the instant we find the pair.

### Why check-then-insert (and not insert-then-check)?

This order matters more than it looks. If you inserted `num` into `seen`
_before_ checking, and `target = 2 * num` (e.g. `nums = [3, 3]`, `target =
6`), you'd match a number against **itself** using the same index — which
violates "can't use the same element twice." Checking first guarantees the
match always comes from a _previously seen_, different index.

## Complexity

- **Time: O(n)** — single pass through the array; each hash map lookup and
  insert is O(1) on average.
- **Space: O(n)** — in the worst case (no match until the very end, or
  values are all distinct), the hash map grows to hold all `n` elements.

This is the classic space-for-time trade: brute force uses O(1) space and
O(n²) time; the hash map approach uses O(n) space to cut that down to O(n)
time.

## Pattern to Remember

**"Have I seen X before?" → hash map, not nested loops.**

This shows up constantly:

- Two Sum (this problem) — seen numbers → index
- Contains Duplicate — seen numbers → boolean
- Longest Consecutive Sequence — seen numbers → used to skip re-counting streaks
- Group Anagrams — seen sorted-string "signature" → list of words

Whenever brute force involves re-scanning an array/string to answer "does
this exist?" or "have I encountered this?", a hash map almost always turns
an O(n²) or O(n log n) solution into O(n).

## Edge Cases Handled

- **Duplicate values that sum to target** (`[3, 3]`, target `6`) — handled
  correctly by the check-before-insert order above.
- **Negative numbers / zero** — works fine, since dict keys and lookups
  don't care about sign.
- Assumes exactly one valid answer exists (per problem constraints), so no
  handling for "no pair found" is needed — but in production code you'd want
  to return `None` or raise if `remaining in seen` never triggers.

## What I Got Wrong / Things to Watch

_(fill this in yourself if anything tripped you up — e.g. did you first try
insert-then-check and hit the duplicate-index bug? Did you forget `enumerate`
and manually track `i`? This section is more useful the more honest it is.)_
