def split_bill(total: int, people: int, tip_percent: int) -> tuple[int, int]:
    """回傳 (每人付多少, 總共多收幾元)，兩者都是 int。"""
    total = round(total * (1 + tip_percent/100))
    pay = ((total+ people -1) // people)
    return pay, pay * people - total