# python gRPC mathfunc.proto client for linear regression

from __future__ import print_function
import logging
import grpc
import time

import mathfunc_pb2
import mathfunc_pb2_grpc

class grpc_linearregression_client:
    def __init__(self) -> None:
        self._description="Linear regression"

    @property
    def description(self)->str:
        return self._description

    def run(self,function_id:int,config)->mathfunc_pb2.State:
        # open connection to gRPC server
        with grpc.insecure_channel('localhost:'+config['GRPCLINREGPORT']) as channel:
            # get communication channel
            stub=mathfunc_pb2_grpc.MathFuncStub(channel)
            fd=mathfunc_pb2.FunctionDescription()
            fd.id=function_id
            state=stub.GuessFunction(fd)
            return state

    def delete(self,config)->mathfunc_pb2.DelState:
        # open connection to gRPC server
        with grpc.insecure_channel('localhost:'+config['GRPCLINREGPORT']) as channel:
            # get communication channel
            stub=mathfunc_pb2_grpc.MathFuncStub(channel)
            dl=mathfunc_pb2.DelMsg()
            return stub.Delete(dl)