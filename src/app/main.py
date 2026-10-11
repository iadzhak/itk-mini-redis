from concurrent import futures

import grpc
from cachetools import LRUCache

from app.core import get_logger, settings
from app.proto import kvstore_pb2_grpc
from app.servicer import KeyValueStoreServicer
from app.storage import MemoryStorage

logger = get_logger(__name__)


def serve():
    logger.info("Инициализация...")
    storage = MemoryStorage(LRUCache(settings.LRU_EVICTION))
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=settings.MAX_WORKERS or None)
    )
    kvstore_pb2_grpc.add_KeyValueStoreServicer_to_server(
        KeyValueStoreServicer(storage), server
    )
    server.add_insecure_port("[::]:" + settings.PORT)
    server.start()
    logger.info("Сервер запущен на порту: %s", settings.PORT)
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        pass
    logger.info("Сервер остановлен")


if __name__ == "__main__":
    serve()
