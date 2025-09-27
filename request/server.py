# server.py
import asyncio
import time
from concurrent import futures

import grpc
import user_pb2
import user_pb2_grpc

# Implementasi service
class UserService(user_pb2_grpc.UserServiceServicer):
    async def Process(self, request, context):
        start = time.time()
        # Validasi sederhana
        if not request.name:
            msg = "name required"
            return user_pb2.UserResponse(ok=False, message=msg, processing_ms=0)

        # Simulasi pemrosesan (IO-bound atau CPU-bound ringan).
        # Ganti atau hilangkan sleep ini sesuai kebutuhan industri/staging.
        await asyncio.sleep(0.01)  # 10 ms simulate

        processing_ms = int((time.time() - start) * 1000)
        msg = f"processed {request.name}"
        return user_pb2.UserResponse(ok=True, message=msg, processing_ms=processing_ms)


async def serve(host="0.0.0.0", port=50051):
    server = grpc.aio.server()
    user_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)
    listen_addr = f"{host}:{port}"
    server.add_insecure_port(listen_addr)
    print(f"[server] starting on {listen_addr}")
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    try:
        asyncio.run(serve())
    except KeyboardInterrupt:
        print("Shutting down server")

