import os
import time
import logging
import subprocess
from concurrent import futures

import grpc
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "generated"))
import proxmox_pb2
import proxmox_pb2_grpc

GRPC_PORT = int(os.environ.get("GRPC_PORT", "50051"))

class ProxmoxManagerServicer(proxmox_pb2_grpc.ProxmoxManagerServicer):
    def run_command(self, command):
        try:
            result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            success = result.returncode == 0
            message = result.stdout.strip() if success else result.stderr.strip()
            return success, message
        except Exception as e:
            return False, str(e)

    def StartVM(self, request, context):
        success, message = self.run_command(f"qm start {request.vmid}")
        return proxmox_pb2.ActionResponse(success=success, message=message)

    def StopVM(self, request, context):
        success, message = self.run_command(f"qm stop {request.vmid}")
        return proxmox_pb2.ActionResponse(success=success, message=message)

    def GetStatus(self, request, context):
        success, output = self.run_command(f"qm status {request.vmid}")
        status = output.strip() if success else "error"
        return proxmox_pb2.StatusResponse(success=success, status=status)

def serve():
    logging.basicConfig(level=logging.INFO)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    proxmox_pb2_grpc.add_ProxmoxManagerServicer_to_server(ProxmoxManagerServicer(), server)
    bind_addr = f"[::]:{GRPC_PORT}"
    server.add_insecure_port(bind_addr)
    logging.info(f"gRPC server running on {bind_addr}")
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == "__main__":
    serve()

