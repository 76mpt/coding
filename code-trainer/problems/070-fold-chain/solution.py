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


def fold_chain(head):
    """把鏈對折重排成 L0 -> Ln-1 -> L1 -> Ln-2 -> ...，回傳新的鏈頭。"""
    # TODO
    return head
