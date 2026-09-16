def top_k_words(text: str, k: int) -> list[tuple[str, int]]:
    """回傳出現次數前 k 名的 (單字, 次數)。"""
    result = {}
    text_list = text.split()
    for word in text_list:
        word = word.lower()
        result[word] = result.get(word, 0) + 1
    ans = sorted(result.items(), key=lambda x: (-x[1], x[0]))
    return ans[:k]
