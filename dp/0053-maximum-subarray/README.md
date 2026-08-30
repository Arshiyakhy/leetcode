# 53. Maximum Subarray

**Link:** https://leetcode.com/problems/maximum-subarray/
**Difficulty:** Medium
**Topic:** Array, Dynamic Programming (Kadane's Algorithm)

## Problem

Given an integer array `nums`, find the contiguous subarray (containing at
least one number) with the largest sum, and return that sum.

```
Input:  nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
Output: 6        # subarray [4, -1, 2, 1] sums to 6
```

## The Brute Force (and why we don't stop there)

Check every possible contiguous subarray:

```python
max_sum = float('-inf')
for i in range(len(nums)):
    for j in range(i, len(nums)):
        max_sum = max(max_sum, sum(nums[i:j+1]))
```

That's **O(n³)** as written (O(n²) subarrays, each summed in O(n)), or
O(n²) if you accumulate the sum incrementally in the inner loop instead of
calling `sum()` each time. Either way, we're redoing a lot of overlapping
work: subarrays starting near each other share huge chunks of the same
sum.

## The Key Insight

This is **Kadane's Algorithm**, and the insight is a single question asked
at every index:

> "Is it better to extend the subarray I was already building, or to
> throw it away and start fresh from here?"

If your running sum (`curSum`) has gone **negative**, it can only be
_dragging down_ any future subarray it's attached to — so the best move is
to abandon it and restart from the current number. If it's still
non-negative, it's worth keeping, because adding it to the next number can
only help (or at worst do nothing).

This is what makes it dynamic programming: `curSum` at each index depends
only on `curSum` at the _previous_ index (plus the current number) — a
classic optimal-substructure relationship, computed in one pass instead of
recomputing every subarray from scratch.

## Walkthrough of the Code

```python
maxSub, curSum = nums[0], 0
for num in nums:
    if curSum < 0:
        curSum = 0
    curSum += num
    maxSub = max(maxSub, curSum)
return maxSub
```

- `maxSub` is initialized to `nums[0]` — this correctly handles all-negative
  arrays (more on this below), since it guarantees the answer starts as a
  real value from the array, not an artificial `0`.
- `curSum` tracks the sum of "the best subarray ending right here."
- On each number:
  1. **Reset if negative** — if `curSum` dropped below `0`, it would only
     hurt to keep it, so reset to `0` (i.e., start a fresh subarray at the
     current number).
  2. **Extend** — add the current number to `curSum`.
  3. **Update the answer** — `maxSub` tracks the best `curSum` seen at any
     point, not just the final one, since the best subarray might end
     earlier than the last index.

### Trace through `[-2, 1, -3, 4, -1, 2, 1, -5, 4]`

| num | curSum < 0? (reset?) | curSum after += num | maxSub       |
| --- | -------------------- | ------------------- | ------------ |
| -2  | curSum=0, no reset   | 0 + (-2) = -2       | -2 (initial) |
| 1   | yes (curSum=-2) → 0  | 0 + 1 = 1           | 1            |
| -3  | no                   | 1 + (-3) = -2       | 1            |
| 4   | yes (curSum=-2) → 0  | 0 + 4 = 4           | 4            |
| -1  | no                   | 4 + (-1) = 3        | 4            |
| 2   | no                   | 3 + 2 = 5           | 5            |
| 1   | no                   | 5 + 1 = 6           | **6**        |
| -5  | no                   | 6 + (-5) = 1        | 6            |
| 4   | no                   | 1 + 4 = 5           | 6            |

Final answer: `6` — matches `[4, -1, 2, 1]`.

## Complexity

- **Time: O(n)** — a single pass, constant work per element.
- **Space: O(1)** — only two running variables (`maxSub`, `curSum`), no
  extra arrays. This is the theoretical best possible for this problem —
  you can't do better than O(n) time since you must inspect every element
  at least once (an adversary could hide the max anywhere).

## Pattern to Remember

**"Extend or restart?" → Kadane's Algorithm: a running value that resets
whenever carrying it forward would only hurt.**

This is a slightly different flavor of the "running accumulator" pattern
seen in Best Time to Buy/Sell Stock — there, the running value (`lowest`)
only ever got _better_ (smaller) and never reset. Here, the running value
can actively become a liability, so it gets reset to `0` at the point it
turns negative. The shared theme: **avoid recomputing from scratch by
carrying forward exactly the amount of state needed to make the next
decision.**

Related problems that build directly on this idea:

- Maximum Subarray (this problem) — classic Kadane's
- Maximum Product Subarray — same idea, but must track both running max
  _and_ running min (because multiplying by a negative can flip which one
  becomes the new max)
- Best Time to Buy and Sell Stock — the "reset when it stops helping"
  cousin, applied to a running minimum instead of a running sum

## Edge Cases Handled

- **All negative numbers** (`[-1]`, `[-3, -2, -1]`) — because `maxSub`
  starts at `nums[0]` (a real array value) rather than `0`, the answer
  correctly comes out as the _least negative_ single element, instead of
  incorrectly returning `0` (which isn't a valid subarray sum here, since
  the problem requires at least one element).
- **Single element** (`[1]`) — loop runs once, `curSum` becomes `1`,
  `maxSub` becomes `1`. Correct.
- **All positive / increasing sums** (`[5, 4, -1, 7, 8]`) — `curSum` never
  needs to reset, and the whole array ends up being the answer (`23`).

## What I Got Wrong / Things to Watch

_(fill in anything that tripped you up here — e.g. did you initially
initialize `maxSub` to `0` and get a wrong answer on an all-negative test
case?)_
