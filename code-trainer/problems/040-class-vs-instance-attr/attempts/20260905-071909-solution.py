class Dataset:
    """一個資料集。name 和 samples 是每個實例自己的，count 是全部共用的。"""

    count = 0          # 類別屬性：建過幾個 Dataset

    def __init__(self, name):
        # TODO: 存 name、建立這個實例自己的 samples、把 count 加 1
        self.name = name
        self.samples = []
        Dataset.count += 1

    def add(self, sample):
        self.samples.append(sample)

    def __len__(self):
        return len(self.samples)


def build_datasets(specs: list) -> tuple[list, int]:
    """specs 是 [(名字, [樣本,...]), ...]。回傳 (datasets, Dataset.count)。"""
    # TODO: 先把 Dataset.count 歸零，再建立
    Dataset.count = 0
    datasets = []
    for name, samples in specs:
        ds = Dataset(name)
        for s in samples:
            ds.add(s)
        datasets.append(ds)
    return datasets, Dataset.count
