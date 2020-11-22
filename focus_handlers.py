from typing import Awaitable, Callable
from i3ipc.aio.connection import Connection
from typing import Union, Dict
from i3ipc.con import Con
import operator


# FIXME: gaps json not working with i3ipc?
inner_gaps = 25
outer_gaps = -5

async def _on_focus_left(connection: Connection):
        # TODO: pass root as param instead of the connection itself?
        #       it will save one await?
        root = await connection.get_tree()
        focused = root.find_focused()

        # check if this is the furthest left container
        if focused.rect.x - (inner_gaps + outer_gaps) > focused.root().rect.x:

            # check if there is a sibling to the left
            parent: Con = focused.parent
            if focused.window_rect.x > parent.window_rect.x:
                await connection.command("focus left")
                
            # otherwise get the closest rightmost container
            else:
                app_windows = root.leaves()
                
                def my_filter(w: Con) -> bool:
                    in_scratchpad = w in root.scratchpad().descendants()
                    is_left_of_focused = w.rect.x < focused.rect.x and w.rect.y <= focused.rect.y
                    return is_left_of_focused and not in_scratchpad
                                
                possible_windows = list(filter(my_filter, app_windows))
                sorted_windows = sorted(possible_windows, key=lambda w: (w.rect.x, w.rect.y))
                
                if len(sorted_windows):
                    await sorted_windows.pop().command("focus")
                             
                
async def _on_focus_right(connection: Connection):
        root = await connection.get_tree()
        focused = root.find_focused()

        # check if this is the furthest right container
        if focused.rect.x + focused.rect.width + inner_gaps + outer_gaps < focused.root().rect.width:
            
            # check if there is a sibling to the left
            parent: Con = focused.parent
            if focused.window_rect.width + focused.rect.x < parent.window_rect.width:
                await connection.command("focus right")
            else:
                app_windows = root.leaves()
                
                def my_filter(w: Con) -> bool:
                    in_scratchpad = w in root.scratchpad().descendants()
                    is_right_of_focused = w.rect.x > focused.rect.width and w.rect.y <= focused.rect.y
                    return is_right_of_focused and not in_scratchpad
                                
                possible_windows = list(filter(my_filter, app_windows))
                sorted_windows = sorted(possible_windows, key=lambda w: (-w.rect.x, w.rect.y))
                
                if len(sorted_windows):
                    await sorted_windows.pop().command("focus")
           
# TODO: have the focus up and down favor the left most possible window the same way
#       the left and right focus favor the top most window
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

def print_container(con: Con):
    print(f"name: {con.window_instance}\n   x: {con.rect.x}, y: {con.rect.y}, w: {con.rect.width} h: {con.rect.height}")