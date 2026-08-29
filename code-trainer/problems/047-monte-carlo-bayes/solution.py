import random


def simulate_posterior(prior: float, sensitivity: float, specificity: float,
                       n: int, seed: int) -> tuple:
    """模擬 n 個人，回傳 (陽性中有病的比例, 陽性人數)。沒人陽性時第一項是 None。"""
    # TODO: rng = random.Random(seed)；每個人抽兩次；數 positive 和 (positive and sick)
