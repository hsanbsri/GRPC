
# Grpc & Rest API

How to install

1. Turn on server
-> cd server1
-> docker-compose build -> docker-compose up

2. Run Shell
chmod +x start_failover.sh -> 
./start_failover.sh


Look at http://127.0.0.1:5000/status for status cpu server 1
if > 80 server 2 on look at here http://127.0.0.1:5001/status

## optional if need

Dashboard http://127.0.0.1:8080
