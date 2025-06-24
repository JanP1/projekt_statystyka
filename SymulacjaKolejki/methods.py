import random
import math


def rozklad_wykladniczy(lambd):
    if lambd <= 0:
        raise ValueError("lambda musi być > 0")
    u = random.random()
    return -math.log(u) / lambd


def minuty_na_godzine(minuty):
    godz = 9 + (minuty // 60)
    min = minuty % 60
    return f"{godz:02d}:{min:02d}"


