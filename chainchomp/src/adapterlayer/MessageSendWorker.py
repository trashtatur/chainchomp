import asyncio
from queue import Empty
from threading import Thread
from time import sleep

from chainchomplib import LoggerInterface
from chainchomplib.adapterlayer.Message import Message
from chainchomplib.data import SocketEvents

from chainchomp.src.adapterlayer.SocketInterface import SocketInterface


class MessageSendWorker(Thread):
    def __init__(self, socket_interface: SocketInterface):
        super().__init__()
        self.is_running = True
        self.socket_interface = socket_interface

    def stop_worker(self):
        self.is_running = False

    def run(self) -> None:
        while self.is_running:
            try:
                message: Message = self.socket_interface.messages_to_send_to_adapters.get(timeout=3)
            except Empty:
                LoggerInterface.warning('No messages to send to adapters')
                sleep(1)
                continue
            else:
                """
                This works in both directions because a client has to declare the adapter as the recipient.
                And the adapter specifies the clients chainlink name as the recipient
                """
                print('found message')
                for recipient in message.message_header.recipients:
                    print(f'sending message to {recipient}')
                    connection = self.socket_interface.get_adapter_connection_by_adapter_name(
                        message.message_header.adapter_name
                    )
                    if connection is not None:
                        print(f'found connection of {message.message_header.adapter_name}. Sending now!')
                        asyncio.run(self.socket_interface.adapter_socket_io.emit(
                            SocketEvents.EMIT_TO_ADAPTER, message.get_serialized(), room=connection.sid
                        ))
