def numerical_derivative(f, x: float, h: float = 1e-5) -> float:
    """用數值方法近似 f'(x)。"""
    return (f(x + h) - f(x - h))/(2 * h)