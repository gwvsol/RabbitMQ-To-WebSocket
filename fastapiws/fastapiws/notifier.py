import asyncio
from typing import List
from starlette.websockets import WebSocket
from starlette.websockets import WebSocketState
from websockets.exceptions import ConnectionClosedOK, \
                                  ConnectionClosedError
from .queue import WSQueue
from .amqp import AMQPClient
from .apiwork import OpenApiWork
from .log import logger


class Notifier:
    """ Рассылка данных в WebSocket """
    def __init__(self):
        self.connections: List[WebSocket] = list()
        self.log = logger
        self._is_ready = False
        self.queue = WSQueue()
        self.db = OpenApiWork()
        self.amqp = AMQPClient(self.queue)

    async def add(self, websocket: WebSocket):
        """ Добавление клиента WebSocket в очередь """
        await websocket.accept()
        self.connections.append(websocket)
        # await self.db.sendAllDataWebSocket(websocket)
        if not self._is_ready:
            await self._iteration()

    def remove(self, websocket: WebSocket):
        """ Удаление клиента WebSocket из очереди """
        try:
            self.connections.remove(websocket)
        except ValueError as err:
            self.log.error(f"ERROR => {err}")

    async def _iteration(self):
        """ Перебор клиентов WebSocket и отправка данных """
        self._is_ready = True
        await self.amqp.connect()
        while self._is_ready:
            living_connections = []
            while len(self.connections) > 0:
                websocket = self.connections.pop()
                try:
                    if websocket.client_state == WebSocketState.CONNECTED:
                        packet = await self.queue.get()
                        if len(packet) > 0:
                            await websocket.send_json(packet)
                        living_connections.append(websocket)
                except (ConnectionClosedOK, ConnectionClosedError) as err:
                    self.log.error(f"ERROR => {err}")
                await asyncio.sleep(0.001)
            self.connections = living_connections
            if len(self.connections) == 0:
                await self.amqp.disconnect()
                self._is_ready = False
            await asyncio.sleep(0.001)
