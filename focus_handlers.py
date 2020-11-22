from typing import Awaitable, Callable
from i3ipc.aio.connection import Connection
from typing import Union, Dict


# FIXME: gaps json not working with i3ipc?
inner_gaps = 25
outer_gaps = -5

async def _on_focus_left(connection: Connection):    
        root = await connection.get_tree()
        focused = root.find_focused()

        if focused.rect.x - (inner_gaps + outer_gaps) > focused.root().rect.x:
            await connection.command("focus left")

async def _on_focus_right(connection: Connection):
        root = await connection.get_tree()
        focused = root.find_focused()

        if focused.rect.x + focused.rect.width + inner_gaps + outer_gaps < focused.root().rect.width:
            await connection.command("focus right")

async def _on_focus_up(connection: Connection):
        root = await connection.get_tree()
        focused = root.find_focused()

        if focused.rect.y - (inner_gaps + outer_gaps) > focused.root().rect.y:
            await connection.command("focus up")

async def _on_focus_down(connection: Connection):
        root = await connection.get_tree()
        focused = root.find_focused()
        max_height = focused.workspace().rect.height
        
        if focused.rect.y + focused.rect.height + inner_gaps + outer_gaps < max_height:
            await connection.command("focus down")

direction_mapper: Dict[str, Callable[[Connection], Awaitable[None]]] = {
    "left": _on_focus_left,
    "right": _on_focus_right,
    "up": _on_focus_up,
    "down": _on_focus_down
}

def get_focus_command(direction: str) -> Union[Callable[[Connection], Awaitable[None]], None]:
    if(direction in direction_mapper.keys()):
        return direction_mapper[direction]
    
    return None
