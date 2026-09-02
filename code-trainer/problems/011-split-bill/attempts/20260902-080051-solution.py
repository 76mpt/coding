def split_bill(total: int, people: int, tip_percent: int) -> tuple[int, int]:
    """回傳 (每人付多少, 總共多收幾元)，兩者都是 int。"""
    total = round(total * (1 + tip_percent/100))
    per_person = round(total // people)
    if total % people > 0:
        per_person += 1
    return per_person, per_person * people - total
