from os import getenv as env


on = ['on', 'On', 'ON', '1', 'True', 'TRUE', 'true']

# =====================================================
GEO_REGION = env('GEO_REGION', default='000000')
# =====================================================
#
# =====================================================
if env('RABBITDB_SERVICE', default='Off') in on:
    RABBITDB_SERVICE = True
else:
    RABBITDB_SERVICE = False
#
RABBITDB_HOST = env('RABBITDB_HOST', default='rabbitdb')
#
RABBITDB_PORT = env('RABBITDB_PORT02', default='5672')
if isinstance(RABBITDB_PORT, str) and RABBITDB_PORT.isdigit():
    RABBITDB_PORT = int(RABBITDB_PORT)
else:
    RABBITDB_PORT = 5672
#
RABBITDB_USER = env('RABBITDB_USER', default='guest')
#
RABBITDB_PASSWORD = env('RABBITDB_PASSWORD', default='guest')
#
RABBITDB_ACTUAL = env('RABBITDB_EXCH_ACTUAL', default='actual')
#
# =====================================================
#
TIMESCALEDB_HOST = env('TIMESCALEDB_HOST', default='timescaledb')
#
TIMESCALEDB_PORT = env('TIMESCALEDB_PORT', default='5432')
#
if isinstance(TIMESCALEDB_PORT, str) and TIMESCALEDB_PORT.isdigit():
    TIMESCALEDB_PORT = int(TIMESCALEDB_PORT)
else:
    TIMESCALEDB_PORT = 5432
#
TIMESCALEDB_USER = env('TIMESCALEDB_USER', default='postgres')
#
TIMESCALEDB_PASWD = env('TIMESCALEDB_PASWD', default='guest')
#
TIMESCALEDB_DBNAME = env('TIMESCALEDB_DBNAME', default='ssmp_geo')
#
# =====================================================
