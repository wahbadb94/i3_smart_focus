import math
from math import sqrt
from typing import Tuple
from i3ipc.con import Con
from i3ipc.model import Rect


def is_left_of(reference: Rect, target: Rect) -> bool:
    return target.x < reference.x


def is_right_of(reference: Rect, target: Rect) -> bool:
    return target.x > reference.x + reference.width


def is_above_of(reference: Rect, target: Rect) -> bool:
    return target.y < reference.y


def is_below_of(reference: Rect, target: Rect) -> bool:
    return target.y > reference.y + reference.height


def window_is_valid_left(reference: Rect, target: Rect) -> bool:
    is_left_of_ref = is_left_of(reference, target)
    is_out_of_bounds_above = (
        is_above_of(reference, target) and target.y + target.height < reference.y
    )
    is_vertically_aligned = not is_out_of_bounds_above and not is_below_of(
        reference, target
    )

    return is_left_of_ref and is_vertically_aligned


def window_is_valid_right(reference: Rect, target: Rect) -> bool:
    is_right_of_ref = is_right_of(reference, target)
    is_out_of_bounds_above = (
        is_above_of(reference, target) and target.y + target.height < reference.y
    )
    is_vertically_aligned = not is_out_of_bounds_above and not is_below_of(
        reference, target
    )

    return is_right_of_ref and is_vertically_aligned


def window_is_valid_below(reference: Rect, target: Rect) -> bool:
    is_below_ref = is_below_of(reference, target)
    is_out_of_bounds_left = (
        is_left_of(reference, target) and target.x + target.width < reference.x
    )
    is_horizontally_aligned = not is_out_of_bounds_left and not is_right_of(
        reference, target
    )

    return is_below_ref and is_horizontally_aligned


def window_is_valid_above(reference: Rect, target: Rect) -> bool:
    is_above_ref = is_above_of(reference, target)
    is_out_of_bounds_left = (
        is_left_of(reference, target) and target.x + target.width < reference.x
    )
    is_horizontally_aligned = not is_out_of_bounds_left and not is_right_of(
        reference, target
    )

    return is_above_ref and is_horizontally_aligned


class Point:
    def __init__(self, x: float, y: float):
        self.x, self.y = x, y


def get_right_midpoint(window: Con) -> Point:
    x = window.rect.x + window.rect.width
    y = window.rect.height / 2.0 + window.rect.y

    return Point(x, y)


def get_left_midpoint(window: Con) -> Point:
    x = window.rect.x
    y = window.rect.height / 2.0 + window.rect.y

    return Point(x, y)


def get_top_midpoint(window: Con) -> Point:
    x = window.rect.width / 2.0 + window.rect.x
    y = window.rect.y

    return Point(x, y)


def get_bottom_midpoint(window: Con) -> Point:
    x = window.rect.width / 2.0 + window.rect.x
    y = window.rect.height + window.rect.y

    return Point(x, y)


def distance_between(p1: Point, p2: Point):
    delta_x = abs(p1.x - p2.x)
    delta_y = abs(p1.y - p2.y)

    return sqrt(delta_x ** 2 + delta_y ** 2)
