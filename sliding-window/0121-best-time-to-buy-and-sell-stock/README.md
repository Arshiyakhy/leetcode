# 121. Best Time to Buy and Sell Stock

**Link:** https://leetcode.com/problems/best-time-to-buy-and-sell-stock/
**Difficulty:** Easy
**Topic:** Array, Sliding Window (Two Pointer)

## Problem

You're given an array `prices` where `prices[i]` is the price of a stock on
day `i`. You may buy the stock on one day and sell it on a later day, to
maximize profit. You must buy before you sell. Return the max profit
achievable, or `0` if no profit is possible.

```
Input:  prices = [7, 1, 5, 3, 6, 4]
Output: 5        # buy at 1 (day 1), sell at 6 (day 4) -> profit 5
```

## The Brute Force (and why we don't stop there)

The obvious idea: try every possible (buy day, sell day) pair.

```python
max_profit = 0
for buy in range(len(prices)):
    for sell in range(buy + 1, len(prices)):
        max_profit = max(max_profit, prices[sell] - prices[buy])
```

That's **O(n²)** — for every buy day, we rescan the rest of the array
looking for the best sell day. For large inputs (LeetCode's constraints go
up to 10^5 prices) this times out. We need to find the answer in a single
pass.

## The Key Insight

This is where the "sliding window" framing helps, even though it doesn't
look like the classic substring-window problems. Think of it as **two
pointers moving together through the array**:

- A pointer tracking the **lowest price seen so far** (this is your best
  possible buy day, up to this point).
- A pointer (`i`, moving forward) representing **today**, the candidate sell
  day.

The window is "from the cheapest day so far up to today." As `i` moves
forward one step at a time, the window's left edge (`lowest`) only ever
moves forward too, and only when it finds something better. This is what
makes it a single-direction sliding window rather than a nested-loop search:
neither pointer ever goes backward, so the whole array is scanned exactly
once.

The reason this is safe (and doesn't miss any answer) is a simple
observation: **the best sell day only cares about the minimum price that
came before it — not which specific earlier day that was.** So instead of
remembering every past price and re-checking each one, you only need to
remember the single smallest price seen so far. That collapses "check every
earlier day" into "check one running value" — the same trade brute force
misses.

## Walkthrough of the Code

```python
if not prices:
    return 0
max_profit = 0
lowest = prices[0]
for i in range(len(prices)):
    if prices[i] < lowest:
        lowest = prices[i]
    current_profit = prices[i] - lowest
    if max_profit < current_profit:
        max_profit = current_profit
return max_profit
```

- `lowest` starts at `prices[0]` — the best (only) buy option on day 0.
- On each day `i`:
  1. **Update the buy price** — if today's price is a new low, that's now
     our best possible buy day going forward.
  2. **Evaluate selling today** — `current_profit = prices[i] - lowest` is
     "if I sell today, having bought at the cheapest point so far, what do I
     make?"
  3. **Update the answer** if this beats everything seen before.
- Because we check "sell today" _before_ moving on, and `lowest` is always
  the minimum from _earlier_ days (today's own price can lower `lowest`,
  but `current_profit` uses the post-update `lowest`, which for today would
  just give `0` — never negative, never invalid).

### Trace through `[7, 1, 5, 3, 6, 4]`

| i   | price | lowest (after update) | current_profit | max_profit |
| --- | ----- | --------------------- | -------------- | ---------- |
| 0   | 7     | 7                     | 0              | 0          |
| 1   | 1     | 1                     | 0              | 0          |
| 2   | 5     | 1                     | 4              | 4          |
| 3   | 3     | 1                     | 2              | 4          |
| 4   | 6     | 1                     | 5              | **5**      |
| 5   | 4     | 1                     | 3              | 5          |

Final answer: `5` — matches buying at day 1 (price 1) and selling at day 4
(price 6).

## Complexity

- **Time: O(n)** — one pass, constant work per element.
- **Space: O(1)** — only two running variables (`lowest`, `max_profit`), no
  extra data structures. This beats a hash-map-based approach in space,
  since here we don't need to look anything up by value — we only ever need
  the single running minimum.

This is actually a step better than problems like Two Sum: there we traded
O(n) space for O(n) time. Here we get O(n) time **and** O(1) space, because
the problem only requires a running aggregate (minimum-so-far), not a
lookup table.

## Pattern to Remember

**"Track a running best/min/max while scanning once" → O(n) single-pass,
no extra structure needed.**

This shows up whenever the answer only depends on a _running statistic_ of
everything before the current index, not on looking up arbitrary past
values:

- Best Time to Buy and Sell Stock (this problem) — running minimum
- Maximum Subarray (Kadane's Algorithm) — running max sum ending here
- Find the Duplicate / running max profit variants

Contrast this with the Two Sum pattern ("have I seen this exact value
before?" → needs a hash map for O(1) lookup by value). Here we don't care
_which_ day had the lowest price, or look anything up by value — we only
ever need one number: the minimum so far. That's what lets this drop all
the way to O(1) space.

## Edge Cases Handled

- **Empty input** (`[]`) — explicit early return of `0`.
- **Single price** (`[5]`) — loop runs once, `current_profit` is always
  `0`, correctly returns `0` (can't buy and sell on the same day for
  profit... well, technically buy and sell same day nets 0, which is
  correct here since you need to buy _before_ you sell).
- **Strictly decreasing prices** (`[7, 6, 4, 3, 1]`) — `current_profit` is
  never positive, so `max_profit` correctly stays `0` instead of going
  negative.

## What I Got Wrong / Things to Watch

_(fill in anything that tripped you up — e.g. did you initially update
`lowest` after computing profit instead of before? Did you forget the empty
list check?)_
