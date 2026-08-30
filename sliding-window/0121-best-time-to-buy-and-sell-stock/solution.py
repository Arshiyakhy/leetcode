"""
121. Best Time to Buy and Sell Stock
https://leetcode.com/problems/best-time-to-buy-and-sell-stock/
"""


class Solution(object):
    def maxProfit(self, prices):
        """
        :type prices: List[int]
        :rtype: int
        """
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


if __name__ == "__main__":
    sol = Solution()

    print(sol.maxProfit([7, 1, 5, 3, 6, 4]))  # 5  (buy at 1, sell at 6)
    # 0  (prices only fall, no profit)
    print(sol.maxProfit([7, 6, 4, 3, 1]))
    print(sol.maxProfit([]))                  # 0  (empty input)
    print(sol.maxProfit([5]))                 # 0  (single price, can't trade)
