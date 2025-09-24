#!/bin/bash

# Threshold CPU
CPU_UPPER=80   # start server2
CPU_LOWER=70   # stop server2

# Interval pengecekan (detik)
CHECK_INTERVAL=10

# Start server1
docker-compose up -d server1
echo "Server1 started..."

SERVER2_UP=0

while true; do
    # Ambil CPU server1
    CPU=$(curl -s http://localhost:5000/status | jq '.cpu_avg')
    CPU_INT=${CPU%.*}
    
    echo "$(date): CPU server1 = $CPU_INT%"

    # Failover: start server2
    if [ "$CPU_INT" -ge "$CPU_UPPER" ] && [ $SERVER2_UP -eq 0 ]; then
        echo "CPU tinggi ($CPU_INT%). Starting server2..."
        docker-compose up -d server2
        SERVER2_UP=1
    fi

    # Failback: stop server2
    if [ "$CPU_INT" -le "$CPU_LOWER" ] && [ $SERVER2_UP -eq 1 ]; then
        echo "CPU rendah ($CPU_INT%). Stopping server2..."
        docker-compose stop server2
        SERVER2_UP=0
    fi

    sleep $CHECK_INTERVAL
done
