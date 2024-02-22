def decodeEmail(e):
    k = int(e[:2], 16)
    return "".join(chr(int(e[i : i + 2], 16) ^ k) for i in range(2, len(e) - 1, 2))