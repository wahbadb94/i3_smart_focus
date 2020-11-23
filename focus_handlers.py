from focus_helpers import (
    window_is_valid_above,
    window_is_valid_below,
    window_is_valid_left,
    window_is_valid_right,
)
from typing import Awaitable, Callable
from i3ipc.aio.connection import Connection
from typing import Union, Dict, List
from i3ipc.con import Con
import os


# FIXME: gaps json not working with i3ipc?
inner_gaps = 25
outer_gaps = -5


async def _on_focus_left(connection: Connection):
    # TODO: pass root as param instead of the connection itself?
    #       it will save one await?
    root = await connection.get_tree()
    focused = root.find_focused()

    # only move if not leftmost window
    if focused.rect.x - (inner_gaps + outer_gaps) > focused.root().rect.x:

        def is_left_filter(w: Con) -> bool:
            return (
                window_is_valid_left(focused.rect, w.rect)
                and w not in root.scratchpad().descendents()
            )

        app_windows = root.leaves()
        possible_windows = list(filter(is_left_filter, app_windows))
        sorted_windows = sorted(
            possible_windows, key=lambda w: (w.rect.x + w.rect.width, -w.rect.y)
        )

        if len(sorted_windows):
            display_windows(focused, sorted_windows)
            await sorted_windows.pop().command("focus")


async def _on_focus_right(connection: Connection):
    root = await connection.get_tree()
    focused = root.find_focused()

    if (
        focused.rect.x + focused.rect.width + inner_gaps + outer_gaps
        < focused.root().rect.width
    ):

        def is_right_filter(w: Con) -> bool:
            return (
                window_is_valid_right(focused.rect, w.rect)
                and w not in root.scratchpad().descendents()
            )

        app_windows = root.leaves()
        possible_windows = list(filter(is_right_filter, app_windows))

        # sort by leftmost then topmost
        # TODO: filter using distance,  see sketch in project folder
        sorted_windows = sorted(possible_windows, key=lambda w: (-w.rect.x, -w.rect.y))

        # if list ain't empty, pop the best window and focus it
        if len(sorted_windows):
            display_windows(focused, sorted_windows)
            await sorted_windows.pop().command("focus")


# TODO: have the focus up and down favor the left most possible window the same way
#       the left and right focus favor the top most window
async def _on_focus_up(connection: Connection):
    root = await connection.get_tree()
    focused = root.find_focused()

    if focused.rect.y - (inner_gaps + outer_gaps) > focused.root().rect.y:

        def is_above_filter(w: Con) -> bool:
            return (
                window_is_valid_above(focused.rect, w.rect)
                and w not in root.scratchpad().descendants()
            )

        app_windows = root.leaves()
        possible_windows = list(filter(is_above_filter, app_windows))
        sorted_windows = sorted(
            possible_windows, key=lambda w: (w.rect.y + w.rect.height, -w.rect.x)
        )

        if len(sorted_windows):
            display_windows(focused, sorted_windows)
            await sorted_windows.pop().command("focus")


async def _on_focus_down(connection: Connection):
    root = await connection.get_tree()
    focused = root.find_focused()
    max_height = focused.workspace().rect.height

    if focused.rect.y + focused.rect.height + inner_gaps + outer_gaps < max_height:

        def is_below_filter(w: Con) -> bool:
            return (
                window_is_valid_below(focused.rect, w.rect)
                and w not in root.scratchpad().descendents()
            )

        app_windows = root.leaves()
        possible_windows = list(filter(is_below_filter, app_windows))
        sorted_windows = sorted(possible_windows, key=lambda w: (-w.rect.y, w.rect.x))

        if len(sorted_windows):
            display_windows(focused, sorted_windows)
            await sorted_windows.pop().command("focus")


direction_mapper: Dict[str, Callable[[Connection], Awaitable[None]]] = {
    "left": _on_focus_left,
    "right": _on_focus_right,
    "up": _on_focus_up,
    "down": _on_focus_down,
}


def get_focus_command(
    direction: str,
) -> Union[Callable[[Connection], Awaitable[None]], None]:
    if direction in direction_mapper.keys():
        return direction_mapper[direction]

    return None


def print_container(con: Con):
    print(
        f"name: {con.window_instance}\n   x: {con.rect.x}, y: {con.rect.y}, w: {con.rect.width} h: {con.rect.height}"
    )


def display_windows(focused: Con, potential_windows: List[Con]):
    os.system("clear")
    print_container(focused)
    print("\n")

    for c in potential_windows:
        print_container(c)
