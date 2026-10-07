import random


def simulate_posterior(prior: float, sensitivity: float, specificity: float,
                       n: int, seed: int) -> tuple:
    """模擬 n 個人，回傳 (陽性中有病的比例, 陽性人數)。沒人陽性時第一項是 None。"""
    # TODO: rng = random.Random(seed)；每個人抽兩次；數 positive 和 (positive and sick)
    pos = 0
    sick_count = 0
    rng = random.Random(seed)
    for _ in range(n):
        sick = rng.random() < prior
        if sick:
            positive = rng.random() < sensitivity
        else:
            positive = rng.random() < (1 - specificity)
        if positive:
            pos += 1
            if sick:
                sick_count += 1
    if pos == 0:
        return None, 0
    return sick_count / pos, pos
        
