"""
105. Construct Binary Tree from Preorder and Inorder Traversal
https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/
"""


class TreeNode(object):
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution(object):
    def buildTree(self, preorder, inorder):
        """
        :type preorder: List[int]
        :type inorder: List[int]
        :rtype: Optional[TreeNode]
        """
        if not preorder or not inorder:
            return None

        root = TreeNode(preorder[0])
        mid = inorder.index(preorder[0])
        root.left = self.buildTree(preorder[1:mid + 1], inorder[:mid])
        root.right = self.buildTree(preorder[mid + 1:], inorder[mid + 1:])
        return root

    def buildTreeOptimal(self, preorder, inorder):
        """
        Optimal O(n) version: hashmap for O(1) index lookups, index
        pointers instead of slicing to avoid copying arrays.
        """
        inorder_index = {val: i for i, val in enumerate(inorder)}
        self.pre_idx = 0

        def helper(in_left, in_right):
            if in_left > in_right:
                return None

            root_val = preorder[self.pre_idx]
            self.pre_idx += 1
            root = TreeNode(root_val)

            mid = inorder_index[root_val]
            root.left = helper(in_left, mid - 1)
            root.right = helper(mid + 1, in_right)
            return root

        return helper(0, len(inorder) - 1)


def to_preorder(root):
    """Helper: convert a tree back to a preorder list, for verifying results."""
    if not root:
        return []
    return [root.val] + to_preorder(root.left) + to_preorder(root.right)


def to_inorder(root):
    """Helper: convert a tree back to an inorder list, for verifying results."""
    if not root:
        return []
    return to_inorder(root.left) + [root.val] + to_inorder(root.right)


if __name__ == "__main__":
    sol = Solution()

    preorder1, inorder1 = [3, 9, 20, 15, 7], [9, 3, 15, 20, 7]
    t1 = sol.buildTree(preorder1, inorder1)
    print(to_preorder(t1), to_inorder(t1))  # matches preorder1, inorder1

    t1_opt = sol.buildTreeOptimal(preorder1, inorder1)
    print(to_preorder(t1_opt), to_inorder(t1_opt))  # same result

    preorder2, inorder2 = [-1], [-1]
    t2 = sol.buildTree(preorder2, inorder2)
    print(to_preorder(t2), to_inorder(t2))  # [-1] [-1]
