import asyncio
from resize_helpers import (
    handle_resize_down,
    handle_resize_left,
    handle_resize_right,
    handle_resize_up,
)
from focus_helpers import is_leftmost_sibling, is_rightmost_sibling

from i3ipc.aio import Connection
from i3ipc import Event
from i3ipc.events import BindingEvent, BindingInfo
from constants import COMMAND_REDIRECTOR, RESIZE_SYMBOLS


async def resize_focused(
    connection: Connection, symbol: str, resize_amount: int
) -> None:
    if symbol not in RESIZE_SYMBOLS:
        return

    root = await connection.get_tree()
    focused = root.find_focused()

    if symbol == "Left":
        await handle_resize_left(focused, resize_amount)
    elif symbol == "Right":
        await handle_resize_right(focused, resize_amount)
    elif symbol == "Up":
        await handle_resize_up(focused, resize_amount)
    elif symbol == "Down":
        await handle_resize_down(focused, resize_amount)


async def main():
    async def on_binding_event(connection: Connection, binding_event: BindingEvent):
        # parse command
        command: str = binding_event.binding.command
        i3_command = command[len(COMMAND_REDIRECTOR) :]
        command_words = i3_command.strip().split(" ")

        if command_words[0] == "resize":
            symbol = binding_event.binding.symbol
            resize_amount = int(command_words[1])
            await resize_focused(connection, symbol, resize_amount)

    connection = await Connection(auto_reconnect=True).connect()
    connection.on(Event.BINDING, on_binding_event)

    await connection.main()


asyncio.get_event_loop().run_until_complete(main())
