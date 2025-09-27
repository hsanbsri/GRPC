#!/bin/bash

while true; do
    CPU_LOAD=$(top -bn1 | grep "Cpu(s)" | awk '{print int(100 - $8)}')

    # cek status VM di Proxmox 2
    status=$(python3 grpc-proxmox/client.py status 200 | awk '{print $NF}')

    if [$CPU_LOAD -gt 80] && [status=stopped]; then
        echo "CPU load tinggi! Menyalakan server2..."
        python3 grpc-proxmox/client.py start 200;
    elif [$CPU_LOAD -lt 60] && [status=running]; then
        python3 grpc-proxmox/client.py stop 200;
    fi

    sleep 10
done
