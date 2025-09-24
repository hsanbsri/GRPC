#!/bin/bash

# Start server1
docker-compose up -d server1

while true; do
    CPU_LOAD=$(curl -s http://localhost:5000/status | jq .cpu)

    echo "Current CPU load: $CPU_LOAD%"

    # Threshold CPU untuk failover
    THRESHOLD=80

    if (( $(echo "$CPU_LOAD > $THRESHOLD" | bc -l) )); then
        echo "CPU load tinggi! Menyalakan server2..."
        docker-compose up -d server2
    fi

    sleep 5
done
