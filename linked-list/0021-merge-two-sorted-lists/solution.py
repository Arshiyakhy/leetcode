"""
21. Merge Two Sorted Lists
https://leetcode.com/problems/merge-two-sorted-lists/
"""


class ListNode(object):
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution(object):
    def mergeTwoLists(self, list1, list2):
        """
        :type list1: Optional[ListNode]
        :type list2: Optional[ListNode]
        :rtype: Optional[ListNode]
        """
        if list1 is None:
            return list2
        if list2 is None:
            return list1

        if list1.val <= list2.val:
            list1.next = self.mergeTwoLists(list1.next, list2)
            return list1
        else:
            list2.next = self.mergeTwoLists(list1, list2.next)
            return list2


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

    # [1,1,2,3,4,4]
    print(to_list(sol.mergeTwoLists(
        build_list([1, 2, 4]), build_list([1, 3, 4]))))
    print(to_list(sol.mergeTwoLists(build_list([]), build_list([])))
          )                  # []
    print(to_list(sol.mergeTwoLists(build_list([]), build_list([0])))
          )                 # [0]
