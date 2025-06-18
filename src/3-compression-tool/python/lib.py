def char_count(s: str) -> dict:
    result = {}
    for char in s:
        result[char] = result.get(char, 0) + 1
    return result