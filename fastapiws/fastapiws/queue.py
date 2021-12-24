from asyncio import Queue, QueueEmpty
from .log import logger


class WSQueue(object):

    def __init__(self) -> None:
        self.queue = Queue()
        self.log = logger

    async def add(self, packet: dict):
        """ Добавляем данные в очередь """
        await self.queue.put(packet)

    async def get(self) -> dict:
        """ Получение данных из очереди """
        packet = dict()
        try:
            packet = self.queue.get_nowait()
        except (QueueEmpty, KeyboardInterrupt):
            pass
        return packet
