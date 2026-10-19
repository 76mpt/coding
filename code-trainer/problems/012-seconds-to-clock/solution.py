def seconds_to_clock(seconds: int) -> str:
    """把秒數轉成 "HH:MM:SS"。"""
    # TODO
    pass
    minute = seconds // 60
    seconds %= 60
    hour = minute // 60
    minute %= 60
    return f"{hour:02}:{minute:02}:{seconds:02}"