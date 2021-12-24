import json
from aio_pika import connect_robust, \
                     ExchangeType, \
                     IncomingMessage
from aio_pika.connection import Connection
from aio_pika.channel import Channel
from aio_pika.exchange import Exchange
from aio_pika.queue import Queue
from .log import logger
from .config import RABBITDB_HOST, \
                    RABBITDB_PORT, \
                    RABBITDB_USER, \
                    RABBITDB_PASSWORD, \
                    RABBITDB_ACTUAL


class AMQPClient(object):
    """ Получения данных с RabbitMQ """
    def __init__(self, queue):
        self.host = RABBITDB_HOST
        self.port = RABBITDB_PORT
        self.user = RABBITDB_USER
        self.passwd = RABBITDB_PASSWORD
        self.exchange = RABBITDB_ACTUAL
        self.log = logger
        self.connection = None
        self.wsqueue = queue
        self.queue_name = None

    async def decode(self, packet: bytearray) -> dict:
        """ Преобразование данных для добавления в очередь """
        packet = packet.decode("utf-8")
        packet = json.loads(packet)
        return packet

    async def connect(self):
        """ Подключение к RabbitMQ, к обменнику и очереди """
        self.connection: Connection = \
            await connect_robust(host=self.host,
                                 port=self.port,
                                 login=self.user,
                                 password=self.passwd)
        self.channel: Channel = await self.connection.channel()
        await self.channel.set_qos(prefetch_count=1)
        exchange: Exchange = \
            await self.channel.declare_exchange(self.exchange,
                                                ExchangeType.FANOUT)
        self.queue: Queue = \
            await self.channel.declare_queue(exclusive=True,
                                             auto_delete=False)
        await self.queue.bind(exchange)
        self.tag = await self.queue.consume(self.callback)
        self.queue_name = self.queue.name
        self.log.info(f"connect => {self.queue_name} | tag => {self.tag}")

    async def callback(self, message: IncomingMessage):
        """ Обработка полученных данных из RabbitMQ """
        async with message.process(ignore_processed=True):
            packet = message.body
            packet = await self.decode(packet)
            await self.wsqueue.add(packet)
            # self.log.info(f"{packet} => {self.tag}")
            await message.ack()

    async def disconnect(self):
        """ Отключение от RabbitMQ, обменника, очереди """
        conn_is_closed = self.connection.is_closed
        if not conn_is_closed:
            ch_is_closed = self.channel.is_closed
            if not ch_is_closed:
                await self.channel.close()
                self.log.info(f"closed => {self.tag}")
            await self.connection.close()
            self.connection = None
        self.log.info(f"disconnect => {self.queue_name} | {self.tag}")
        self.queue_name = None
