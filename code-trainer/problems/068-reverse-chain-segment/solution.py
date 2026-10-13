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


def reverse_between(head, left, right):
    """把鏈上第 left 到第 right 個節點原地反轉，回傳整條鏈的新開頭。"""
    # TODO
    if head is None:
        return None
    dummy = ListNode(0, head)
    prev = dummy
    for _ in range(left - 1):
        prev = prev.next
    curr = prev.next
    for _ in range(right - left):
        move = curr.next
        curr.next = move.next
        move.next = prev.next
        prev.next = move
    return dummy.next
