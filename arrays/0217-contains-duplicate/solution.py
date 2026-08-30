"""
217. Contains Duplicate
https://leetcode.com/problems/contains-duplicate/
"""


class Solution(object):
    def containsDuplicate(self, nums):
        """
        :type nums: List[int]
        :rtype: bool
        """
        s = set()
        for n in nums:
            if n in s:
                return True
            s.add(n)
        return False


if __name__ == "__main__":
    sol = Solution()

    print(sol.containsDuplicate([1, 2, 3, 1]))        # True  (1 appears twice)
    print(sol.containsDuplicate([1, 2, 3, 4]))         # False (all distinct)
    print(sol.containsDuplicate([1, 1, 1, 3, 3, 4, 3, 2, 4, 2]))  # True
    print(sol.containsDuplicate([]))                   # False (empty input)
