import os

import socketio
from aiohttp import web
from chainchomplib import LoggerInterface
from chainchomplib.adapterlayer.Message import Message
from chainchomplib.adapterlayer.MessageDeserializer import MessageDeserializer
from chainchomplib.adapterlayer.MessageHeader import MessageHeader
from chainchomplib.configlayer.ChainfileDeserializer import ChainfileDeserializer
from chainchomplib.configlayer.resolver.AdapterResolver import AdapterResolver
from chainchomplib.data import SocketEvents
from chainchomplib.data.RemoteChainfileDTO import RemoteChainfileDTO

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


@routes.post('/chainfile/remote/receive')
async def assign_link_to_adapter(request):
    """
    This endpoint receives a remote chainfile
    """
    data: dict = await request.json()
    data_is_next = data.get('is_next', False)
    data_is_previous = data.get('is_previous', False)
    if not data_is_next and not data_is_previous:
        return web.Response(
            reason='The data has to specify if it is addressing a previous or a next chainlink',
            status=403
        )

    if data_is_next == data_is_previous:
        return web.Response(
            reason='The receiving chainlink can\'t be next and also previous.',
            status=403
        )
    data_name_of_called_link = data.get('name_of_called_link', None)
    if data_name_of_called_link is None:
        return web.Response(reason='The called links name needs to be specified', status=403)

    chainfile_model = ChainfileDeserializer.deserialize(data.get('chainfile', {}))
    if not chainfile_model:
        return web.Response(reason='The data did not have a serialized chainfile', status=403)

    if not chainfile_model.adapter:
        return web.Response(reason='The serialized model had no adapter', status=403)

    adapter_connection = socket_interface.get_adapter_connection_by_adapter_name(chainfile_model.adapter)
    if not adapter_connection:
        adapter_model = AdapterResolver.resolve(chainfile_model.adapter)
        sentence_inlay = ''
        if adapter_model is not None:
            sentence_inlay = 'The Server will attempt to start this adapter. Please try again.'
            os.system(adapter_model.start)
        return web.Response(
            reason=f'No matching adapter is currently connected. {sentence_inlay}',
            status=500
        )
    remote_chainfile_dto = RemoteChainfileDTO(
        chainfile_model,
        data_is_next,
        data_is_previous,
        request.remote,
        data_name_of_called_link
    )
    await sio.emit(SocketEvents.EMIT_REMOTE_CHAINFILE_TO_ADAPTER, remote_chainfile_dto.get_serialized())
    return web.Response(status=200)


@routes.post('/chainfile/local/receive')
async def configure_adapter(request):
    """
    This endpoint receives a local chainfile
    """
    data = await request.json()
    chainfile_model = ChainfileDeserializer.deserialize(data.get('chainfile', {}))
    if not chainfile_model:
        return web.Response(reason='The data did not have a serialized chainfile', status=403)

    if not chainfile_model.adapter:
        return web.Response(reason='The serialized model had no adapter', status=403)

    if not chainfile_model.chainlink_name:
        return web.Response(reason='The serialized model had no chainlink name', status=403)

    adapter_connection = socket_interface.get_adapter_connection_by_adapter_name(chainfile_model.adapter)
    if not adapter_connection:
        adapter_model = AdapterResolver.resolve(chainfile_model.adapter)
        sentence_inlay = ''
        if adapter_model is not None:
            sentence_inlay = 'The Server will attempt to start this adapter. Please try again.'
            os.system(adapter_model.start)
        return web.Response(
            reason=f'No matching adapter is currently connected. {sentence_inlay}',
            status=500
        )
    return web.Response(status=200)


@sio.event
async def connect(sid, environ: dict):
    adapter = environ.get('HTTP_CHAINCHOMP_ADAPTER', None)
    chainlink_name = environ.get('HTTP_CHAINLINK_NAME', None)
    if adapter is not None and chainlink_name is not None:
        LoggerInterface.error(f'{sid} has supplied a wrong configuration of headers to connect. Disconnecting')
        await sio.disconnect(sid)
    if chainlink_name is None and adapter is None:
        LoggerInterface.error(f'{sid} did not supply adapter or chainlink name. Disconnecting')
        await sio.disconnect(sid)
    if adapter is not None:
        socket_interface.activate_adapter_connection(
            Connection(sid, True, adapter)
        )
    if chainlink_name is not None:
        socket_interface.activate_client_connection(
            Connection(sid, True, chainlink_name)
        )


@sio.event
async def disconnect(sid):
    LoggerInterface.info(f'{sid} has disconnected')
    socket_interface.deactivate_adapter_connection(sid)


@sio.on(SocketEvents.RECEIVE_MESSAGE_FROM_ADAPTER)
async def receive_message_from_adapter(socket_id, data):
    message = MessageDeserializer.deserialize(data)
    if message is not None:
        socket_interface.queue_message_to_client_application(data)
        LoggerInterface.info(f'Received message from adapter with socket id {socket_id}')
    else:
        LoggerInterface.error(f'Received incorrect data from {socket_id}: {data}')


@sio.on(SocketEvents.RECEIVE_MESSAGE_FROM_CHAINLINK)
async def receive_message_from_chainlink(socket_id, data):
    message = MessageDeserializer.deserialize(data)
    if message is not None:
        socket_interface.queue_message_to_adapter(data)
        LoggerInterface.info(f'Received message from chainlink with socket id {socket_id}')
    else:
        LoggerInterface.error(f'Received incorrect data from {socket_id}: {data}')


if __name__ == '__main__':
    app.add_routes(routes)
    web.run_app(app, port=4410)
