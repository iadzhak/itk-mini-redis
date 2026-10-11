# @pytest.fixture(scope='module')
# def grpc_add_to_server():
#     from app.proto.kvstore_pb2_grpc import add_KeyValueStoreServicer_to_server
#
#     return add_KeyValueStoreServicer_to_server
#
#
# @pytest.fixture(scope='module')
# def grpc_servicer():
#     from app.servicer import KeyValueStoreServicer
#
#     return KeyValueStoreServicer()
#
#
# @pytest.fixture(scope='module')
# def grpc_stub_cls(grpc_channel):
#     from app.proto.kvstore_pb2_grpc import KeyValueStoreStub
#
#     return KeyValueStoreStub
