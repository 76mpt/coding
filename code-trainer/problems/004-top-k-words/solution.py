def top_k_words(text: str, k: int) -> list[tuple[str, int]]:
    """回傳出現次數前 k 名的 (單字, 次數)。"""
    result = {}
    for word in text.lower().split():
        result[word] = result.get(word, 0) + 1
    result = sorted(result.items(), key=lambda x:(-x[1], x[0]))
    return result[:k]
