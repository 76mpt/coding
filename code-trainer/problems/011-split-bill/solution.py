def split_bill(total: int, people: int, tip_percent: int) -> tuple[int, int]:
    """回傳 (每人付多少, 總共多收幾元)，兩者都是 int。"""
    # TODO
    pass
    amount = round(total * (1 + tip_percent/100))
    per = int(-amount // people) * -1
    remain = int(per * people - amount)
    return per, remain
    
