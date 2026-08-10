def seconds_to_clock(seconds: int) -> str:
    """把秒數轉成 "HH:MM:SS"。"""
    minutes = seconds // 60
    seconds = seconds % 60
    hours = minutes // 60
    minutes = minutes % 60
    return (f"{hours:02}:{minutes:02}:{seconds:02}")