"""
98. Validate Binary Search Tree
https://leetcode.com/problems/validate-binary-search-tree/
"""

from collections import deque


class TreeNode(object):
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution(object):
    def isValidBST(self, root):
        """
        :type root: Optional[TreeNode]
        :rtype: bool
        """
        def valid(node, left, right):
            if not node:
                return True
            if not (left < node.val < right):
                return False
            return valid(node.left, left, node.val) and valid(node.right, node.val, right)

        return valid(root, float("-inf"), float("inf"))


def build_tree(values):
    """Helper: build a binary tree from a level-order list (None = missing node)."""
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    q = deque([root])
    i = 1
    while q and i < len(values):
        node = q.popleft()
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            q.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            q.append(node.right)
        i += 1
    return root


if __name__ == "__main__":
    sol = Solution()

    print(sol.isValidBST(build_tree([2, 1, 3])))              # True
    # False (4 is in the right subtree of 5, so must be > 5, but 4 < 5)
    print(sol.isValidBST(build_tree([5, 1, 4, None, None, 3, 6])))
    print(sol.isValidBST(build_tree([1])))                     # True
    # False (equal values not allowed, must be strictly less/greater)
    print(sol.isValidBST(build_tree([2, 2, 2])))
