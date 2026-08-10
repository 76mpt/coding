def seconds_to_clock(seconds: int) -> str:
    """把秒數轉成 "HH:MM:SS"。"""
    # TODO
    minutes = seconds // 60
    seconds = seconds % 60
    hours = minutes // 60
    minutes = minutes % 60
    return (f"{hours:02d}:{minutes:02d}:{seconds:02d}")
    pass
