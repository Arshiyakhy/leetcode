"""
19. Remove Nth Node From End of List
https://leetcode.com/problems/remove-nth-node-from-end-of-list/
"""


class ListNode(object):
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution(object):
    def removeNthFromEnd(self, head, n):
        """
        :type head: Optional[ListNode]
        :type n: int
        :rtype: Optional[ListNode]
        """
        N = 0
        cur = head
        while cur:
            N += 1
            cur = cur.next

        removeIndex = N - n
        if removeIndex == 0:
            return head.next

        cur = head
        for i in range(N - 1):
            if (i + 1) == removeIndex:
                cur.next = cur.next.next
                break
            cur = cur.next
        return head


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

    # [1, 2, 3, 5]
    print(to_list(sol.removeNthFromEnd(build_list([1, 2, 3, 4, 5]), 2)))
    print(to_list(sol.removeNthFromEnd(build_list([1]), 1)))               # []
    print(to_list(sol.removeNthFromEnd(
        build_list([1, 2]), 1)))            # [1]
    # [2] (remove head)
    print(to_list(sol.removeNthFromEnd(build_list([1, 2]), 2)))
