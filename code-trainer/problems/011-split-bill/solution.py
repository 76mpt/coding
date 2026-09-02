def split_bill(total: int, people: int, tip_percent: int) -> tuple[int, int]:
    """回傳 (每人付多少, 總共多收幾元)，兩者都是 int。"""
    total_tip = round(total * (1 + tip_percent / 100))
    extra = 0
    if total_tip % people != 0:
        per_person = -(-(total_tip // people) - 1)
        extra = per_person * people - total_tip 
    else:
        per_person = total_tip / people
    return per_person, extra    
