"""
238. Product of Array Except Self
https://leetcode.com/problems/product-of-array-except-self/
"""


class Solution(object):
    def productExceptSelf(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """
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


if __name__ == "__main__":
    sol = Solution()

    print(sol.productExceptSelf([1, 2, 3, 4]))       # [24, 12, 8, 6]
    print(sol.productExceptSelf([-1, 1, 0, -3, 3]))  # [0, 0, 9, 0, 0]
    print(sol.productExceptSelf([2, 3]))              # [3, 2]
    # [1]  (no other elements)
    print(sol.productExceptSelf([5]))
