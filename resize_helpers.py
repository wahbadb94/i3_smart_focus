from i3ipc.con import Con
from focus_helpers import (
    is_bottommost_sibling,
    is_leftmost_sibling,
    is_rightmost_sibling,
    is_topmost_sibling,
)


async def handle_resize_left(window: Con, resize_amount: int):
    # resize parent if only child or if parent is split vertically
    parent: Con = window.parent
    if len(parent.nodes) == 1 or parent.ipc_data["layout"] == "splitv":
        await handle_resize_left(parent, resize_amount)

    elif is_leftmost_sibling(window):
        await window.command(
            f"resize shrink width {resize_amount} px or {resize_amount} ppt"
        )
    elif is_rightmost_sibling(window):
        await window.command(
            f"resize grow width {resize_amount} px or {resize_amount} ppt"
        )


async def handle_resize_right(window: Con, resize_amount: int):
    # resize parent if only child or if parent is split vertically
    parent: Con = window.parent

    if len(parent.nodes) == 1 or parent.ipc_data["layout"] == "splitv":
        await handle_resize_right(parent, resize_amount)

    elif is_rightmost_sibling(window):
        await window.command(
            f"resize shrink width {resize_amount} px or {resize_amount} ppt"
        )
    elif is_leftmost_sibling(window):
        await window.command(
            f"resize grow width {resize_amount} px or {resize_amount} ppt"
        )


async def handle_resize_up(window: Con, resize_amount: int):
    # resize parent if only child or if parent is split horizontally
    parent: Con = window.parent
    if len(parent.nodes) == 1 or parent.ipc_data["layout"] == "splith":
        await handle_resize_up(parent, resize_amount)

    elif is_topmost_sibling(window):
        await window.command(
            f"resize shrink height {resize_amount} px or {resize_amount} ppt"
        )
    elif is_bottommost_sibling(window):
        await window.command(
            f"resize grow height {resize_amount} px or {resize_amount} ppt"
        )


async def handle_resize_down(window: Con, resize_amount: int):
    # resize parent if only child or if parent is split horizontally
    parent: Con = window.parent
    if len(parent.nodes) == 1 or parent.ipc_data["layout"] == "splith":
        await handle_resize_up(parent, resize_amount)

    elif is_bottommost_sibling(window):
        await window.command(
            f"resize shrink height {resize_amount} px or {resize_amount} ppt"
        )
    elif is_topmost_sibling(window):
        print("topmost")
        await window.command(
            f"resize grow height {resize_amount} px or {resize_amount} ppt"
        )