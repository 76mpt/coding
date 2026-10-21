class ListNode:
    """鏈結串列的節點。測資會用這個類別建鏈，不要改它的 __init__。"""

    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def __repr__(self):
        # 只在測資失敗時用到：讓錯誤訊息印出整條鏈而不是記憶體位址。別刪。
        vals, node, seen = [], self, set()
        while node is not None and id(node) not in seen and len(vals) < 30:
            seen.add(id(node))
            vals.append(str(node.val))
            node = node.next
        return " -> ".join(vals) + (" -> ..." if node is not None else "")


def scan_chain(head):
    """掃描一條鏈，回傳 (has_loop, length, mid_val)。"""
    # TODO
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return (True, -1, None)
    n = 0
    node = head
    while node is not None:
        n += 1
        node = node.next
    return (False, n, slow.val if slow is not None else None)
