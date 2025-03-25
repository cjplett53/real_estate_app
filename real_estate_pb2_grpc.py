# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import real_estate_pb2 as real__estate__pb2

GRPC_GENERATED_VERSION = '1.70.0'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in real_estate_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class RealEstateServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ListProperties = channel.unary_unary(
                '/realestate.RealEstateService/ListProperties',
                request_serializer=real__estate__pb2.ListPropertiesRequest.SerializeToString,
                response_deserializer=real__estate__pb2.ListPropertiesResponse.FromString,
                _registered_method=True)
        self.GetProperty = channel.unary_unary(
                '/realestate.RealEstateService/GetProperty',
                request_serializer=real__estate__pb2.GetPropertyRequest.SerializeToString,
                response_deserializer=real__estate__pb2.GetPropertyResponse.FromString,
                _registered_method=True)
        self.CreateProperty = channel.unary_unary(
                '/realestate.RealEstateService/CreateProperty',
                request_serializer=real__estate__pb2.CreatePropertyRequest.SerializeToString,
                response_deserializer=real__estate__pb2.CreatePropertyResponse.FromString,
                _registered_method=True)
        self.ListAgents = channel.unary_unary(
                '/realestate.RealEstateService/ListAgents',
                request_serializer=real__estate__pb2.ListAgentsRequest.SerializeToString,
                response_deserializer=real__estate__pb2.ListAgentsResponse.FromString,
                _registered_method=True)
        self.GetAgent = channel.unary_unary(
                '/realestate.RealEstateService/GetAgent',
                request_serializer=real__estate__pb2.GetAgentRequest.SerializeToString,
                response_deserializer=real__estate__pb2.GetAgentResponse.FromString,
                _registered_method=True)
        self.CreateAgent = channel.unary_unary(
                '/realestate.RealEstateService/CreateAgent',
                request_serializer=real__estate__pb2.CreateAgentRequest.SerializeToString,
                response_deserializer=real__estate__pb2.CreateAgentResponse.FromString,
                _registered_method=True)
        self.addUser = channel.unary_unary(
                '/realestate.RealEstateService/addUser',
                request_serializer=real__estate__pb2.addUserRequest.SerializeToString,
                response_deserializer=real__estate__pb2.addUserResponse.FromString,
                _registered_method=True)
        self.getUser = channel.unary_unary(
                '/realestate.RealEstateService/getUser',
                request_serializer=real__estate__pb2.getUserRequest.SerializeToString,
                response_deserializer=real__estate__pb2.getUserResponse.FromString,
                _registered_method=True)


class RealEstateServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def ListProperties(self, request, context):
        """Properties
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetProperty(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateProperty(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListAgents(self, request, context):
        """Agents (unused)
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetAgent(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateAgent(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def addUser(self, request, context):
        """login
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getUser(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_RealEstateServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ListProperties': grpc.unary_unary_rpc_method_handler(
                    servicer.ListProperties,
                    request_deserializer=real__estate__pb2.ListPropertiesRequest.FromString,
                    response_serializer=real__estate__pb2.ListPropertiesResponse.SerializeToString,
            ),
            'GetProperty': grpc.unary_unary_rpc_method_handler(
                    servicer.GetProperty,
                    request_deserializer=real__estate__pb2.GetPropertyRequest.FromString,
                    response_serializer=real__estate__pb2.GetPropertyResponse.SerializeToString,
            ),
            'CreateProperty': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateProperty,
                    request_deserializer=real__estate__pb2.CreatePropertyRequest.FromString,
                    response_serializer=real__estate__pb2.CreatePropertyResponse.SerializeToString,
            ),
            'ListAgents': grpc.unary_unary_rpc_method_handler(
                    servicer.ListAgents,
                    request_deserializer=real__estate__pb2.ListAgentsRequest.FromString,
                    response_serializer=real__estate__pb2.ListAgentsResponse.SerializeToString,
            ),
            'GetAgent': grpc.unary_unary_rpc_method_handler(
                    servicer.GetAgent,
                    request_deserializer=real__estate__pb2.GetAgentRequest.FromString,
                    response_serializer=real__estate__pb2.GetAgentResponse.SerializeToString,
            ),
            'CreateAgent': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateAgent,
                    request_deserializer=real__estate__pb2.CreateAgentRequest.FromString,
                    response_serializer=real__estate__pb2.CreateAgentResponse.SerializeToString,
            ),
            'addUser': grpc.unary_unary_rpc_method_handler(
                    servicer.addUser,
                    request_deserializer=real__estate__pb2.addUserRequest.FromString,
                    response_serializer=real__estate__pb2.addUserResponse.SerializeToString,
            ),
            'getUser': grpc.unary_unary_rpc_method_handler(
                    servicer.getUser,
                    request_deserializer=real__estate__pb2.getUserRequest.FromString,
                    response_serializer=real__estate__pb2.getUserResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'realestate.RealEstateService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('realestate.RealEstateService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class RealEstateService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def ListProperties(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/realestate.RealEstateService/ListProperties',
            real__estate__pb2.ListPropertiesRequest.SerializeToString,
            real__estate__pb2.ListPropertiesResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetProperty(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/realestate.RealEstateService/GetProperty',
            real__estate__pb2.GetPropertyRequest.SerializeToString,
            real__estate__pb2.GetPropertyResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def CreateProperty(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/realestate.RealEstateService/CreateProperty',
            real__estate__pb2.CreatePropertyRequest.SerializeToString,
            real__estate__pb2.CreatePropertyResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def ListAgents(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/realestate.RealEstateService/ListAgents',
            real__estate__pb2.ListAgentsRequest.SerializeToString,
            real__estate__pb2.ListAgentsResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetAgent(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/realestate.RealEstateService/GetAgent',
            real__estate__pb2.GetAgentRequest.SerializeToString,
            real__estate__pb2.GetAgentResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def CreateAgent(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/realestate.RealEstateService/CreateAgent',
            real__estate__pb2.CreateAgentRequest.SerializeToString,
            real__estate__pb2.CreateAgentResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def addUser(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/realestate.RealEstateService/addUser',
            real__estate__pb2.addUserRequest.SerializeToString,
            real__estate__pb2.addUserResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def getUser(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/realestate.RealEstateService/getUser',
            real__estate__pb2.getUserRequest.SerializeToString,
            real__estate__pb2.getUserResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
