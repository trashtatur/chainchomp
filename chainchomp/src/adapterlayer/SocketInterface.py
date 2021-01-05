import queue

from chainchomplib.adapterlayer.Message import Message
from socketio import AsyncServer

from chainchomp.src.adapterlayer.Connection import Connection


class SocketInterface:
    __instance = None
    active_adapter_connections = []
    active_chainlink_connections = []
    messages_to_send_to_adapters = queue.Queue()
    messages_to_receive_from_adapters = queue.Queue()
    adapter_socket_io: AsyncServer = None

    def queue_message_to_adapter(self, message: Message):
        self.messages_to_send_to_adapters.put(message)

    def queue_message_to_client_application(self, message: Message):
        self.messages_to_receive_from_adapters.put(message)

    def activate_adapter_connection(self, connection: Connection):
        self.active_adapter_connections.append(connection)

    def activate_client_connection(self, connection: Connection):
        self.active_chainlink_connections.append(connection)

    def deactivate_adapter_connection(self, socket_id):
        self.active_adapter_connections = [
            connection for connection in self.active_adapter_connections
            if connection.sid != socket_id
        ]

    def deactivate_client_connection(self, socket_id):
        self.active_chainlink_connections = [
            connection for connection in self.active_chainlink_connections
            if connection.sid != socket_id
        ]

    def get_adapter_connection_by_adapter_name(self, adapter_name: str) -> Connection or None:
        connection_optional = [
            connection for connection in self.active_adapter_connections
            if connection.adapter_name == adapter_name
        ]
        return connection_optional[0] if len(connection_optional) == 1 else None

    def get_client_application_connection_by_chainlink_name(self, chainlink_name: str) -> Connection or None:
        connection_optional = [
            connection for connection in self.active_chainlink_connections
            if connection.adapter_name == chainlink_name
        ]
        return connection_optional[0] if len(connection_optional) == 1 else None

    def __new__(cls):
        if SocketInterface.__instance is None:
            SocketInterface.__instance = object.__new__(cls)
        return SocketInterface.__instance

