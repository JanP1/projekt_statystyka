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


def w_okolicach_wartosci(liczba):
    percent = random.randint(4, 8)  # random % from 4 to 8
    wartosc = round(liczba * (percent / 100))
    if random.choice([True, False]):  # randomly decide to add or subtract
        return liczba + wartosc
    else:
        return liczba - wartosc
