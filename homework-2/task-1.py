def parse_str(str: str) -> str:
    mid = len(str) // 2
    if len(str) % 2 == 0:
        return str[mid - 1 : mid + 1]
    else:
        return str[mid]


print(parse_str("test"), parse_str("testing"))
