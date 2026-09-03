"""
141. Linked List Cycle
https://leetcode.com/problems/linked-list-cycle/
"""


class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution(object):
    def hasCycle(self, head):
        """
        :type head: ListNode
        :rtype: bool
        """
        slow, fast = head, head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow == fast:
                return True
        return False


def build_list_with_cycle(values, pos):
    """Helper: build a linked list from a list of values.
    If pos >= 0, connect the tail's .next to the node at index `pos`
    (creating a cycle), matching LeetCode's `pos` parameter convention.
    """
    if not values:
        return None
    nodes = [ListNode(v) for v in values]
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i + 1]
    if pos >= 0:
        nodes[-1].next = nodes[pos]
    return nodes[0]


if __name__ == "__main__":
    sol = Solution()

    # True  (cycle back to index 1)
    print(sol.hasCycle(build_list_with_cycle([3, 2, 0, -4], 1)))
    # True  (cycle back to index 0)
    print(sol.hasCycle(build_list_with_cycle([1, 2], 0)))
    # False (no cycle, single node)
    print(sol.hasCycle(build_list_with_cycle([1], -1)))
    print(sol.hasCycle(build_list_with_cycle([], -1))
          )             # False (empty list)
