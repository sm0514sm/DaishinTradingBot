def dif_percent(a, b) -> float:
    if 0 in [a, b]:
        return 0
    return (a - b) / b * 100
