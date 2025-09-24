FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Expose ports gRPC dan REST
EXPOSE 50051  
EXPOSE 5000   

# Command to run both REST and gRPC servers
CMD ["sh", "-c", "python grpc_server.py & python app.py"]
