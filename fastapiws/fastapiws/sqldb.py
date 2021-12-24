import asyncpg
import socket
from .config import TIMESCALEDB_HOST, \
                    TIMESCALEDB_PORT, \
                    TIMESCALEDB_USER, \
                    TIMESCALEDB_PASWD, \
                    TIMESCALEDB_DBNAME
from .log import logger


class TimeScaleDB(object):
    """ Класс для работы с базой данных TimescaleDB """
    def __init__(self):
        self.dbconf = {"user": TIMESCALEDB_USER,
                       "password": TIMESCALEDB_PASWD,
                       "host": TIMESCALEDB_HOST,
                       "port": TIMESCALEDB_PORT,
                       "database": TIMESCALEDB_DBNAME,
                       "command_timeout": 60}
        self.log = logger

    async def getAllData(self) -> list:
        """ Получение всех записей из таблицы actual """

        STR = """SELECT car_numder, id_car, alarmbutton, direction,
                        odometer, moving, actual, speed, timecoordinates,
                        valid, latitude, longitude FROM actual"""
        try:
            async with asyncpg.create_pool(**self.dbconf) as pool:
                async with pool.acquire() as con:
                    return await con.fetch(STR)
        except (ConnectionRefusedError, socket.gaierror) as err:
            self.log.error(f'<= {err}')
            return dict({'error': f'{err}'})
