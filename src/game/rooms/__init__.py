import logging
import math

logger = logging.getLogger(__name__)

def distance_to_line(p0, p1, p) -> float:
    x0, y0 = p0
    x1, y1 = p1
    x, y = p
    return abs((y1 - y0) * x - (x1 - x0) * y + x1 * y0 - y1 * x0) / math.sqrt(
        (y1 - y0) ** 2 + (x1 - x0) ** 2
    )


def in_range(x, x0, x1):
    return min(x0, x1) <= x <= max(x0, x1)