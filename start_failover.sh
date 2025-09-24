#!/bin/bash

CPU_THRESHOLD=80
CHECK_INTERVAL=5

# Start server1 dulu
docker-compose up -d server1
SERVER2_UP=0

while true; do
    CPU=$(curl -s http://localhost:5000/status | python -c "import sys,json; print(int(json.load(sys.stdin)['cpu_avg']))")
    
    if [ -z "$CPU" ]; then
        echo "Gagal ambil CPU"
        sleep $CHECK_INTERVAL
        continue
    fi

    echo "$(date): CPU server1 = $CPU%"

    if [ "$CPU" -ge "$CPU_THRESHOLD" ] && [ $SERVER2_UP -eq 0 ]; then
        echo "CPU tinggi ($CPU%). Starting server2..."
        docker-compose up -d server2
        SERVER2_UP=1
    fi

    if [ "$CPU" -lt "$CPU_THRESHOLD" ] && [ $SERVER2_UP -eq 1 ]; then
        echo "CPU rendah ($CPU%). Stopping server2..."
        docker-compose stop server2
        SERVER2_UP=0
    fi

    sleep $CHECK_INTERVAL
done
