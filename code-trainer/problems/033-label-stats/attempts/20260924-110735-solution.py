def label_stats(labels: list[int], num_classes: int) -> tuple[bool, int, set]:
    """回傳 (是否全部合法, 合法的數量, 相異的合法標籤集合)。"""
    # TODO: 分別用 all / sum / set comprehension，三行
    legal = all(0 <= label < num_classes for label in labels)
    num = sum(1 for label in labels if 0 <= label < num_classes)
    sets = {label for label in labels if 0 <= label < num_classes}
    return legal, num, sets