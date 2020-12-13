import socketio
from aiohttp import web
from chainchomplib import LoggerInterface

from chainchomp.src.adapterlayer import ServerEvents
from chainchomp.src.adapterlayer.MessageReceiveWorker import MessageReceiveWorker
from chainchomp.src.adapterlayer.MessageSendWorker import MessageSendWorker
from chainchomp.src.adapterlayer.SocketInterface import SocketInterface
from chainchomp.src.adapterlayer.Connection import Connection

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)
socket_interface = SocketInterface()
socket_interface.adapter_socket_io = sio
message_receive_worker = MessageReceiveWorker(socket_interface)
message_send_worker = MessageSendWorker(socket_interface)
message_receive_worker.start()
message_send_worker.start()
routes = web.RouteTableDef()


@routes.get('/adapter/assign/link')
async def hello(request):
    return web.Response(text="Hello, world")


@sio.event
async def connect(sid, environ: dict):
    print(environ)
    adapter = environ.get('HTTP_CHAINCHOMP_ADAPTER', None)
    chainlink_name = environ.get('HTTP_CHAINLINK_NAME', None)
    if adapter is not None and chainlink_name is not None:
        LoggerInterface.error(f'{sid} has supplied a wrong configuration of headers to connect. Disconnecting')
        await sio.disconnect(sid)
    if adapter is not None:
        socket_interface.activate_adapter_connection(
            Connection(sid, True, adapter)
        )
    if chainlink_name is not None:
        socket_interface.active_chainlink_connections(
            Connection(sid, True, chainlink_name)
        )
    if chainlink_name is None and adapter is None:
        LoggerInterface.error(f'{sid} did not supply adapter or chainlink name')
        await sio.disconnect(sid)


@sio.event
async def disconnect(sid):
    LoggerInterface.info(f'{sid} has disconnected')
    socket_interface.deactivate_adapter_connection(sid)


@sio.on(ServerEvents.RECEIVE_MESSAGE_FROM_ADAPTER)
async def receive_message_from_adapter(socket_id, data):
    socket_interface.queue_message_to_client_application(data)
    LoggerInterface.info(f'Received message from adapter with socket id {socket_id}')


@sio.on(ServerEvents.RECEIVE_MESSAGE_FROM_CHAINLINK)
async def receive_message_from_chainlink(socket_id, data):
    socket_interface.queue_message_to_adapter(data)
    LoggerInterface.info(f'Received message from chainlink with socket id {socket_id}')


if __name__ == '__main__':
    app.add_routes(routes)
    web.run_app(app, port=4410)
