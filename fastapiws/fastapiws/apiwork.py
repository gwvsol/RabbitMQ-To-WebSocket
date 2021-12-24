from time import time
from geojson import Point
from asyncpg import Record
from starlette.websockets import WebSocket
from .log import logger
from .sqldb import TimeScaleDB


class OpenApiWork(object):

    def __init__(self):
        self.logger = logger
        self._sqldb = TimeScaleDB()
        self._getAllDataTime = time()
        self._getAllDataTimeMax = 120

    async def formatWebSocketData(self, data: Record) -> list:
        """ Форматирование данных для отправки в WebSocket """

        rcv = list()
        for r in data:
            _, id_car, alarmbutton, direction,\
                odometer, _, _, speed, timecoordinates,\
                valid, latitude, longitude = tuple(r)
            rcv.append(dict(
                Valid=valid, Direction=direction, AlarmButton=alarmbutton,
                Id=id_car, Speed=speed, Time=str(timecoordinates),
                Odometer=odometer, coordinates=Point((longitude, latitude))
            ))
        self.logger.info(f"COUNT => {len(data)}")
        return rcv

    async def getWebSocketData(self):
        """ Получение данных из TimescaleDB из
            таблицы actual для WebSocket """
        self._getAllDataTime = time()
        data = await self._sqldb.getAllData()
        return await self.formatWebSocketData(data)

    async def sendAllDataWebSocket(self, websocket: WebSocket):
        datas = await self.getWebSocketData()
        if len(datas) > 0:
            for data in datas:
                await websocket.send_json(data)
