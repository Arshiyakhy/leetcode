"""
206. Reverse Linked List
https://leetcode.com/problems/reverse-linked-list/
"""


class ListNode(object):
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution(object):
    def reverseList(self, head):
        """
        :type head: Optional[ListNode]
        :rtype: Optional[ListNode]
        """
        prev, curr = None, head

        while curr:
            temp = curr.next
            curr.next = prev
            prev = curr
            curr = temp
        return prev


def build_list(values):
    """Helper: build a linked list from a Python list, return the head."""
    dummy = ListNode()
    tail = dummy
    for v in values:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next


def to_list(head):
    """Helper: convert a linked list back into a Python list for printing."""
    result = []
    while head:
        result.append(head.val)
        head = head.next
    return result


if __name__ == "__main__":
    sol = Solution()

    # [5, 4, 3, 2, 1]
    print(to_list(sol.reverseList(build_list([1, 2, 3, 4, 5]))))
    print(to_list(sol.reverseList(build_list([1, 2]))))            # [2, 1]
    print(to_list(sol.reverseList(build_list([]))))                # []
