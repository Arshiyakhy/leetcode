"""
143. Reorder List
https://leetcode.com/problems/reorder-list/
"""


class ListNode(object):
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution(object):
    def reorderList(self, head):
        """
        :type head: Optional[ListNode]
        :rtype: None  Do not return anything, modify head in-place instead.
        """
        # Step 1: find the middle of the list (fast/slow pointers)
        slow, fast = head, head.next
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        # Step 2: reverse the second half
        second = slow.next
        prev = slow.next = None
        while second:
            tmp = second.next
            second.next = prev
            prev = second
            second = tmp

        # Step 3: merge the two halves, alternating nodes
        first, second = head, prev
        while second:
            tmp1, tmp2 = first.next, second.next
            first.next = second
            second.next = tmp1
            first, second = tmp1, tmp2


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

    head1 = build_list([1, 2, 3, 4])
    sol.reorderList(head1)
    print(to_list(head1))  # [1, 4, 2, 3]

    head2 = build_list([1, 2, 3, 4, 5])
    sol.reorderList(head2)
    print(to_list(head2))  # [1, 5, 2, 4, 3]

    head3 = build_list([1])
    sol.reorderList(head3)
    print(to_list(head3))  # [1]

    head4 = build_list([1, 2])
    sol.reorderList(head4)
    print(to_list(head4))  # [1, 2]
