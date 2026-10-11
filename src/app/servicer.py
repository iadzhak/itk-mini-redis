import functools
import itertools

from google.rpc import code_pb2, status_pb2
from grpc_status import rpc_status

from app.core import get_logger
from app.proto.kvstore_pb2 import (  # type: ignore[attr-defined]
    DeleteResponse,
    GetResponse,
    KeyValue,
    ListResponse,
    PutResponse,
)
from app.proto.kvstore_pb2_grpc import KeyValueStoreServicer as BaseServicer
from app.storage import BaseStorage


class KeyValueStoreServicer(BaseServicer):
    _logger = get_logger(__name__)
    _counter = itertools.count()

    def __init__(self, storage: BaseStorage):
        self._s = storage

    @staticmethod
    def logger(func):
        @functools.wraps(func)
        def wrapper(self, request, context):
            _id = next(KeyValueStoreServicer._counter)
            KeyValueStoreServicer._logger.info(
                '%s - %s\t| %s\t| %s', 'in', _id, func.__name__, str(request).strip()
            )
            try:
                result = func(self, request, context)
                KeyValueStoreServicer._logger.info(
                    '%s - %s\t| %s\t| %s',
                    'out',
                    _id,
                    func.__name__,
                    str(result).strip(),
                )
                return result
            except Exception as e:
                KeyValueStoreServicer._logger.warning(
                    '%s - %s\t| %s\t| %s', 'err', _id, func.__name__, str(e)
                )
                raise

        return wrapper

    @logger
    def Put(self, request, context):
        self._s.put(request.key, request.value, request.ttl_seconds)
        return PutResponse()

    @logger
    def Get(self, request, context):
        value = self._s.get(request.key)
        if value is None:
            context.abort_with_status(
                rpc_status.to_status(status_pb2.Status(code=code_pb2.NOT_FOUND))
            )
        return GetResponse(value=value)

    @logger
    def Delete(self, request, context):
        self._s.delete(request.key)
        return DeleteResponse()

    @logger
    def List(self, request, context):
        response = ListResponse()
        for k, v in self._s.list(request.prefix):
            response.items.append(KeyValue(key=k, value=v))
        return response
