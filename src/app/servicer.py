from app.proto.kvstore_pb2_grpc import KeyValueStoreServicer as BaseServicer
from app.storage import BaseStorage


class KeyValueStoreServicer(BaseServicer):
    def __init__(self, storage: BaseStorage):
        self._s = storage

    def Put(self, request, context):
        pass

    def Get(self, request, context):
        pass

    def Delete(self, request, context):
        pass

    def List(self, request, context):
        pass
