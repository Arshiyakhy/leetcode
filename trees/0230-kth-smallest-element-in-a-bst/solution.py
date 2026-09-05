"""
230. Kth Smallest Element in a BST
https://leetcode.com/problems/kth-smallest-element-in-a-bst/
"""


class TreeNode(object):
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution(object):
    def inorder(self, root):
        result = []

        def _traverse(node):
            if node is None:
                return
            _traverse(node.left)
            result.append(node.val)
            _traverse(node.right)

        _traverse(root)
        return result

    def kthSmallest(self, root, k):
        """
        :type root: Optional[TreeNode]
        :type k: int
        :rtype: int
        """
        result = self.inorder(root)
        return result[k - 1]


def build_bst(values):
    """Helper: build a BST from a list of values via repeated insertion."""
    root = None
    for v in values:
        root = _insert(root, v)
    return root


def _insert(node, val):
    if node is None:
        return TreeNode(val)
    if val < node.val:
        node.left = _insert(node.left, val)
    else:
        node.right = _insert(node.right, val)
    return node


if __name__ == "__main__":
    sol = Solution()

    print(sol.kthSmallest(build_bst([3, 1, 4, 2]), 1))       # 1
    print(sol.kthSmallest(build_bst([5, 3, 6, 2, 4, 1]), 3))  # 3
    print(sol.kthSmallest(build_bst([1]), 1))                 # 1
