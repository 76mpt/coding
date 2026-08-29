class Dataset:
    """一個資料集。name 和 samples 是每個實例自己的，count 是全部共用的。"""

    count = 0          # 類別屬性：建過幾個 Dataset

    def __init__(self, name):
        # TODO: 存 name、建立這個實例自己的 samples、把 count 加 1
        ...

    def add(self, sample):
        # TODO
        ...

    def __len__(self):
        # TODO
        ...


def build_datasets(specs: list) -> tuple[list, int]:
    """specs 是 [(名字, [樣本,...]), ...]。回傳 (datasets, Dataset.count)。"""
    # TODO: 先把 Dataset.count 歸零，再建立
