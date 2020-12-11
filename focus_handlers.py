from focus_helpers import (
    _print_container,
    distance_between,
    get_bottom_midpoint,
    get_left_midpoint,
    get_right_midpoint,
    get_top_midpoint,
    window_is_valid_above,
    window_is_valid_below,
    window_is_valid_left,
    window_is_valid_right,
)
from typing import Awaitable, Callable
from i3ipc.aio.connection import Connection
from typing import Union, Dict
from i3ipc.con import Con


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

        def is_left_of_focused(w: Con) -> bool:
            return (
                window_is_valid_left(focused.rect, w.rect)
                and w not in root.scratchpad().descendents()
            )

        def distance_left_of_focused(w: Con) -> float:
            focused_left_midpoint = get_left_midpoint(focused)
            w_right_midpoint = get_right_midpoint(w)

            return distance_between(focused_left_midpoint, w_right_midpoint)

        app_windows = root.leaves()
        possible_windows = list(filter(is_left_of_focused, app_windows))
        sorted_windows = sorted(
            possible_windows, key=lambda w: (distance_left_of_focused(w), w.rect.y)
        )

        if len(sorted_windows):
            await sorted_windows[0].command("focus")


async def _on_focus_right(connection: Connection):
    root = await connection.get_tree()
    focused = root.find_focused()

    if (
        focused.rect.x + focused.rect.width + inner_gaps + outer_gaps
        < focused.root().rect.width
    ):

        def is_right_of_focused(w: Con) -> bool:
            return (
                window_is_valid_right(focused.rect, w.rect)
                and w not in root.scratchpad().descendents()
            )

        def distance_right_of_focused(w: Con) -> float:
            focused_right_midpoint = get_right_midpoint(focused)
            w_left_midpoint = get_left_midpoint(w)

            return distance_between(focused_right_midpoint, w_left_midpoint)

        app_windows = root.leaves()
        possible_windows = list(filter(is_right_of_focused, app_windows))

        # sort by distance to focused window
        sorted_windows = sorted(
            possible_windows, key=lambda w: (distance_right_of_focused(w), w.rect.y)
        )

        # if list ain't empty, pop the best window and focus it
        if len(sorted_windows):
            await sorted_windows[0].command("focus")


async def _on_focus_up(connection: Connection):
    root = await connection.get_tree()
    focused = root.find_focused()

    parent: Con = focused.parent
    if parent.ipc_data["layout"] == "stacked":
        if focused != parent.nodes[0]:
            await focused.command("focus up")

    elif focused.rect.y - (inner_gaps + outer_gaps) > focused.root().rect.y:
        # func used to filter out windows not above the focused window
        def is_above_focused(w: Con) -> bool:
            return (
                window_is_valid_above(focused.rect, w.rect)
                and w not in root.scratchpad().descendants()
            )

        # func usedto calculate the distance this window is from
        # the currently focused window
        def distance_above_focused(w: Con) -> float:
            focused_top_midpoint = get_top_midpoint(focused)
            w_bottom_midpoint = get_bottom_midpoint(w)

            return distance_between(focused_top_midpoint, w_bottom_midpoint)

        app_windows = root.leaves()
        possible_windows = list(filter(is_above_focused, app_windows))
        sorted_windows = sorted(
            possible_windows, key=lambda w: (distance_above_focused(w), w.rect.x)
        )

        if len(sorted_windows):
            await sorted_windows[0].command("focus")


async def _on_focus_down(connection: Connection):
    root = await connection.get_tree()
    focused = root.find_focused()
    max_height = focused.workspace().rect.height

    parent: Con = focused.parent
    if parent.ipc_data["layout"] == "stacked":
        if focused != parent.nodes[-1]:
            await focused.command("focus down")

    if focused.rect.y + focused.rect.height + inner_gaps + outer_gaps < max_height:

        def is_below_focused(w: Con) -> bool:
            return (
                window_is_valid_below(focused.rect, w.rect)
                and w not in root.scratchpad().descendants()
            )

        def distance_below_focused(w: Con) -> float:
            focused_bottom_midpoint = get_bottom_midpoint(focused)
            w_top_midpoint = get_top_midpoint(w)

            return distance_between(focused_bottom_midpoint, w_top_midpoint)

        app_windows = root.leaves()
        possible_windows = list(filter(is_below_focused, app_windows))
        sorted_windows = sorted(
            possible_windows, key=lambda w: (distance_below_focused(w), w.rect.x)
        )

        if len(sorted_windows):
            await sorted_windows[0].command("focus")


_direction_mapper: Dict[str, Callable[[Connection], Awaitable[None]]] = {
    "left": _on_focus_left,
    "right": _on_focus_right,
    "up": _on_focus_up,
    "down": _on_focus_down,
}


def get_focus_command(
    direction: str,
) -> Union[Callable[[Connection], Awaitable[None]], None]:
    if direction in _direction_mapper.keys():
        return _direction_mapper[direction]

    return None
