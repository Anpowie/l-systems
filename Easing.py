import math
from Vector import Vec


def easeOutCubic(x) -> float:
    return 1 - math.pow(1 - x, 3)


def easeInCubic(x) -> float:
    return x * x * x


def lerp(a, b, p) -> float:
    return a + (b - a) * p


def lerpVec(posA, posB, p) -> Vec:
    return Vec(
        lerp(posA.x, posB.x, p),
        lerp(posA.y, posB.y, p)
    )
