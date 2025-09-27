import os
import grpc
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "generated"))
import proxmox_pb2
import proxmox_pb2_grpc

# export GRPC_HOST="proxmox_ip:50051"
GRPC_HOST = os.environ.get("GRPC_HOST", "localhost:50051")

def get_stub():
    channel = grpc.insecure_channel(GRPC_HOST)
    return proxmox_pb2_grpc.ProxmoxManagerStub(channel)

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 client.py start|stop <vmid>")
        sys.exit(1)

    action = sys.argv[1].lower()
    vmid_str = sys.argv[2]

    if not vmid_str.isdigit():
        print("Error: VMID harus angka.")
        sys.exit(1)

    vmid = int(vmid_str)

    stub = get_stub()

    if action == "start":
        resp = stub.StartVM(proxmox_pb2.VMRequest(vmid=vmid))
        print(f"Start VM {vmid}: {resp.success} - {resp.message}")

    elif action == "stop":
        resp = stub.StopVM(proxmox_pb2.VMRequest(vmid=vmid))
        print(f"Stop VM {vmid}: {resp.success} - {resp.message}")

    elif action == "status":
        resp = stub.GetStatus(proxmox_pb2.VMRequest(vmid=vmid))
        print(f"Status VM {vmid}: {resp.success} - {resp.status}")

    else:
        print("Error: Action harus 'start', 'stop', atau 'status'.")
        sys.exit(1)
if __name__ == "__main__":
    main()

