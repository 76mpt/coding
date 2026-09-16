def top_k_words(text: str, k: int) -> list[tuple[str, int]]:
    """回傳出現次數前 k 名的 (單字, 次數)。"""
    text = text.lower().split()
    text_dict = {}
    for tex in text:
        text_dict[tex] = text_dict.get(tex, 0) +1
    result = sorted(text_dict.items(), key = lambda item:(-item[1], item[0]))
    return result[:k]
    

