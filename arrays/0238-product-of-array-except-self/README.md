# 238. Product of Array Except Self

**Link:** https://leetcode.com/problems/product-of-array-except-self/
**Difficulty:** Medium
**Topic:** Array, Prefix Sum / Prefix Product

## Problem

Given an integer array `nums`, return an array `answer` such that
`answer[i]` equals the product of all elements of `nums` **except**
`nums[i]`.

```
Input:  nums = [1, 2, 3, 4]
Output: [24, 12, 8, 6]
```

**Constraints that shape the solution:**

- Must run in **O(n)** time.
- **Cannot use division** (otherwise the "obvious" trick — compute the
  total product, then divide by `nums[i]` for each index — would be
  trivial). Division is banned partly because it breaks if any element is
  `0`.

## The Brute Force (and why we don't stop there)

For each index `i`, multiply together every element except `nums[i]`:

```python
result = []
for i in range(len(nums)):
    product = 1
    for j in range(len(nums)):
        if i != j:
            product *= nums[j]
    result.append(product)
```

That's **O(n²)** — for every index, we redo an O(n) multiplication pass.
We're re-deriving "product of everything except index i" from scratch each
time, when most of that work overlaps with the previous index's work.

## The Key Insight

`answer[i]` = (product of everything **before** `i`) × (product of
everything **after** `i`).

Split into two halves:

- **prefix[i]** = product of `nums[0..i-1]` (everything to the left of `i`)
- **suffix[i]** = product of `nums[i+1..n-1]` (everything to the right of `i`)

If you had both arrays, `answer[i] = prefix[i] * suffix[i]`.

The trick for computing `prefix` in one pass: `prefix[i]` is just
`prefix[i-1] * nums[i-1]` — each prefix product builds directly on the one
before it, so you never need to re-multiply from the start. Same idea for
`suffix`, scanning right to left.

This is the same "running accumulator" idea as Best Time to Buy and Sell
Stock — instead of recomputing a range product from scratch for every `i`
(brute force), you carry forward one running value and update it
incrementally.

## Walkthrough of the Code

```python
n = len(nums)
result = [1] * n

prefix = 1
for i in range(n):
    result[i] = prefix
    prefix *= nums[i]

suffix = 1
for i in range(n - 1, -1, -1):
    result[i] *= suffix
    suffix *= nums[i]

return result
```

**Pass 1 — left to right, building prefix products directly into `result`:**

- `prefix` starts at `1` (product of "nothing" before index 0).
- At each `i`, `result[i]` is set to `prefix` — the product of everything
  _strictly before_ `i`.
- _Then_ `prefix` is updated by multiplying in `nums[i]`, so it's ready for
  the next index.
- After this pass, `result[i]` holds exactly `prefix[i]` as defined above.

**Pass 2 — right to left, folding in suffix products:**

- `suffix` starts at `1` (product of "nothing" after the last index).
- At each `i`, `result[i]` gets **multiplied** (not overwritten) by
  `suffix` — combining the prefix product already stored there with the
  suffix product.
- Then `suffix` is updated with `nums[i]` for the next (leftward) index.

The clever part: **`result` is reused as both the prefix array and the
final answer array**, so no second full-size array is needed for `suffix` —
just a single running variable.

### Trace through `[1, 2, 3, 4]`

**Pass 1 (prefix, left to right):**

| i   | prefix (before write) | result[i] | prefix (after update) |
| --- | --------------------- | --------- | --------------------- |
| 0   | 1                     | 1         | 1 × 1 = 1             |
| 1   | 1                     | 1         | 1 × 2 = 2             |
| 2   | 2                     | 2         | 2 × 3 = 6             |
| 3   | 6                     | 6         | 6 × 4 = 24            |

`result` after pass 1: `[1, 1, 2, 6]`

**Pass 2 (suffix, right to left):**

| i   | suffix (before) | result[i] \*= suffix | suffix (after update) |
| --- | --------------- | -------------------- | --------------------- |
| 3   | 1               | 6 × 1 = 6            | 1 × 4 = 4             |
| 2   | 4               | 2 × 4 = 8            | 4 × 3 = 12            |
| 1   | 12              | 1 × 12 = 12          | 12 × 2 = 24           |
| 0   | 24              | 1 × 24 = 24          | 24 × 1 = 24           |

Final `result`: `[24, 12, 8, 6]` ✓ — matches the expected output.

## Complexity

- **Time: O(n)** — exactly two linear passes over the array (still O(n)
  overall, since constants drop out).
- **Space: O(1) extra space** — only two running variables (`prefix`,
  `suffix`). The `result` array doesn't count against space complexity here
  since the problem requires it as the output. (Note: this is why the
  problem is careful to say "the output array does not count as extra
  space" in its full constraints.)

## Pattern to Remember

**"I need info from both directions relative to index i" → do two passes,
one left-to-right and one right-to-left, combining a running accumulator
each time.**

This is a step up from the single-direction running accumulator seen in
Best Time to Buy/Sell Stock — here, the answer at each index depends on
_both_ sides, so one pass isn't enough, but two linear passes still beat
the brute force's nested loop.

Related problems using this two-direction pattern:

- Product of Array Except Self (this problem) — prefix/suffix product
- Trapping Rain Water — prefix max height / suffix max height
- Candy — left-to-right pass then right-to-left pass to satisfy both
  neighbor constraints

## Edge Cases Handled

- **Zero in the array** (`[-1, 1, 0, -3, 3]`) — works correctly without
  division; every index except the one holding `0` gets `0` (since the
  product of everything else must include the zero), and the zero's own
  index gets the product of everything else. No division-by-zero risk
  exists because there's no division at all.
- **Two elements** (`[2, 3]`) — `answer = [3, 2]`, i.e. each index just
  gets the other value. Works naturally since prefix/suffix products of a
  single remaining element are just that element.
- **Single element** (`[5]`) — prefix and suffix both stay `1` throughout
  (no other elements to multiply in), so `answer = [1]` — correct, since
  the product of "everything except itself" in a 1-element array is the
  empty product, `1`.

## What I Got Wrong / Things to Watch

_(fill in anything that tripped you up — e.g. did you initially try to use
division and then have to rework it? Did you first use two separate arrays
for prefix and suffix before realizing you could combine them into
`result`?)_
