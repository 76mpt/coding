def digital_root(n: int) -> tuple[int, int]:
    """回傳 (數位根, 相加的輪數)。"""    
    count = 0
    total = [int(x) for x in str(n)]
    while len(total) > 1:
        result = 0
        for num in total:
            result += num
        count += 1
        total = [int(x) for x in str(result)]
    return total[0], count
    # 標準解 list
    # count = 0
    # while n >= 10:
    #     n = sum(int(value) for value in str(n))
    #     count += 1
    # return n, count

    # num
    #     total = 0
    #     while n > 0:
    #         total += n %10
    #         n //= 10
    #     n = total
    #     count += 1
    # return n, count    