from typing import Callable, Union
from i3ipc.aio import Connection
from i3ipc import Event
import asyncio
from i3ipc.events import BindingEvent
from focus_handlers import get_focus_command
from constants import command_redirector


def parse_binding_event(
    binding_event: BindingEvent,
) -> Union[Callable[[Connection], None], None]:
    command: str = binding_event.binding.command  # exec i3py_redirect focus left
    i3_command = command[len(command_redirector) :]  # focus left
    command_words = i3_command.strip().split(" ")  # ["focus", "left"]

    if command_words[0] == "focus":
        focusable = command_words[1]  # "left"
        return get_focus_command(focusable)  # a callable function


async def main():
    # define our binding event handler
    async def on_binding_event(connection: Connection, binding_event: BindingEvent):
        command: str = binding_event.binding.command

        if command_redirector in command:
            our_command = parse_binding_event(binding_event)
            if our_command is not None:
                await our_command(connection)

    # create connection and subscribe to binding events
    connection = await Connection(auto_reconnect=True).connect()
    connection.on(Event.BINDING, on_binding_event)

    await connection.main()


asyncio.get_event_loop().run_until_complete(main())
