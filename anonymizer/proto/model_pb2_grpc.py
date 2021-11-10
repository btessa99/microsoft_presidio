# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from proto import model_pb2 as proto_dot_model__pb2


class AnonymizerEntityStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.sendRecognizerResults = channel.stream_unary(
                '/AnonymizerEntity/sendRecognizerResults',
                request_serializer=proto_dot_model__pb2.RecognizerResult.SerializeToString,
                response_deserializer=proto_dot_model__pb2.FileAck.FromString,
                )
        self.sendAnonymizedItems = channel.stream_unary(
                '/AnonymizerEntity/sendAnonymizedItems',
                request_serializer=proto_dot_model__pb2.AnonymizedItem.SerializeToString,
                response_deserializer=proto_dot_model__pb2.FileAck.FromString,
                )
        self.sendConfig = channel.unary_unary(
                '/AnonymizerEntity/sendConfig',
                request_serializer=proto_dot_model__pb2.Config.SerializeToString,
                response_deserializer=proto_dot_model__pb2.FileAck.FromString,
                )
        self.sendFile = channel.stream_unary(
                '/AnonymizerEntity/sendFile',
                request_serializer=proto_dot_model__pb2.DataFile.SerializeToString,
                response_deserializer=proto_dot_model__pb2.FileAck.FromString,
                )
        self.getText = channel.unary_stream(
                '/AnonymizerEntity/getText',
                request_serializer=proto_dot_model__pb2.Request.SerializeToString,
                response_deserializer=proto_dot_model__pb2.DataFile.FromString,
                )
        self.getItems = channel.unary_stream(
                '/AnonymizerEntity/getItems',
                request_serializer=proto_dot_model__pb2.Request.SerializeToString,
                response_deserializer=proto_dot_model__pb2.Item.FromString,
                )


class AnonymizerEntityServicer(object):
    """Missing associated documentation comment in .proto file."""

    def sendRecognizerResults(self, request_iterator, context):
        """sends analyzer results
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def sendAnonymizedItems(self, request_iterator, context):
        """sends anonymizer results
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def sendConfig(self, request, context):
        """sends anonymizers or deanonymizers 
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def sendFile(self, request_iterator, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getText(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getItems(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_AnonymizerEntityServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'sendRecognizerResults': grpc.stream_unary_rpc_method_handler(
                    servicer.sendRecognizerResults,
                    request_deserializer=proto_dot_model__pb2.RecognizerResult.FromString,
                    response_serializer=proto_dot_model__pb2.FileAck.SerializeToString,
            ),
            'sendAnonymizedItems': grpc.stream_unary_rpc_method_handler(
                    servicer.sendAnonymizedItems,
                    request_deserializer=proto_dot_model__pb2.AnonymizedItem.FromString,
                    response_serializer=proto_dot_model__pb2.FileAck.SerializeToString,
            ),
            'sendConfig': grpc.unary_unary_rpc_method_handler(
                    servicer.sendConfig,
                    request_deserializer=proto_dot_model__pb2.Config.FromString,
                    response_serializer=proto_dot_model__pb2.FileAck.SerializeToString,
            ),
            'sendFile': grpc.stream_unary_rpc_method_handler(
                    servicer.sendFile,
                    request_deserializer=proto_dot_model__pb2.DataFile.FromString,
                    response_serializer=proto_dot_model__pb2.FileAck.SerializeToString,
            ),
            'getText': grpc.unary_stream_rpc_method_handler(
                    servicer.getText,
                    request_deserializer=proto_dot_model__pb2.Request.FromString,
                    response_serializer=proto_dot_model__pb2.DataFile.SerializeToString,
            ),
            'getItems': grpc.unary_stream_rpc_method_handler(
                    servicer.getItems,
                    request_deserializer=proto_dot_model__pb2.Request.FromString,
                    response_serializer=proto_dot_model__pb2.Item.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'AnonymizerEntity', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class AnonymizerEntity(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def sendRecognizerResults(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_unary(request_iterator, target, '/AnonymizerEntity/sendRecognizerResults',
            proto_dot_model__pb2.RecognizerResult.SerializeToString,
            proto_dot_model__pb2.FileAck.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def sendAnonymizedItems(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_unary(request_iterator, target, '/AnonymizerEntity/sendAnonymizedItems',
            proto_dot_model__pb2.AnonymizedItem.SerializeToString,
            proto_dot_model__pb2.FileAck.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def sendConfig(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/AnonymizerEntity/sendConfig',
            proto_dot_model__pb2.Config.SerializeToString,
            proto_dot_model__pb2.FileAck.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def sendFile(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_unary(request_iterator, target, '/AnonymizerEntity/sendFile',
            proto_dot_model__pb2.DataFile.SerializeToString,
            proto_dot_model__pb2.FileAck.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def getText(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/AnonymizerEntity/getText',
            proto_dot_model__pb2.Request.SerializeToString,
            proto_dot_model__pb2.DataFile.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def getItems(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/AnonymizerEntity/getItems',
            proto_dot_model__pb2.Request.SerializeToString,
            proto_dot_model__pb2.Item.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)