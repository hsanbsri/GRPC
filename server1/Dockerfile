# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements & install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Expose port Flask
EXPOSE 5000

# Command to run
CMD ["python", "app.py"]
