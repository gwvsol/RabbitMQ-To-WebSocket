import logging as logger

log_format = '%(asctime)s.%(msecs)d|\
%(levelname)s|%(module)s.%(funcName)s:%(lineno)d %(message)s'
logger.basicConfig(level=logger.INFO,
                   format=log_format,
                   datefmt='%Y-%m-%d %H:%M:%S')
