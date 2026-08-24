def top_k_words(text: str, k: int) -> list[tuple[str, int]]:
    """回傳出現次數前 k 名的 (單字, 次數)。"""
    total = text.split()
    result = {}
    for tex in total:
        tex = tex.lower()
        result[tex] = result.get(tex, 0) + 1
    answer = (sorted(result.items(), key=lambda item: (-item[1], item[0])))
    return answer[:k]
