import grpc
from concurrent import futures
import time
import service_pb2_grpc, service_pb2

class MyService(service_pb2_grpc.MyServiceServicer):
    def Check(self, request, context):
        return service_pb2.ResponseMessage(message=f"Server alive! CPU load: {request.status}")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_MyServiceServicer_to_server(MyService(), server)
    server.add_insecure_port('[::]:50051')
    print("gRPC server running on port 50051")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
