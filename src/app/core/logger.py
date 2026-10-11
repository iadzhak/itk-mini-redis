import logging

from app.core.config import settings

FMT = '%(asctime)s\t| %(name)s\t| %(levelname)s\t|  %(message)s'
DATEFMT = '%d-%m-%Y %H:%M:%S'


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)

    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(FMT, DATEFMT))

    logger.addHandler(handler)
    logger.setLevel(settings.LOG_LEVEL)

    return logger
