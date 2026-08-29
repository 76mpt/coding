import math

GAMMA = 0.5772156649015329


def series_facts(n: int) -> tuple:
    """回傳 (H_n, H_n - (ln n + γ), 砍半次數)。n = 0 時第二項是 None。"""
    # TODO: 三個分別算
