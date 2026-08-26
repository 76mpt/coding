def label_stats(labels: list[int], num_classes: int) -> tuple[bool, int, set]:
    """回傳 (是否全部合法, 合法的數量, 相異的合法標籤集合)。"""
    # TODO: 分別用 all / sum / set comprehension，三行
