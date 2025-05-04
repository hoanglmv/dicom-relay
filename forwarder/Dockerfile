# Dockerfile cho service forwarder
FROM python:3.10-slim

WORKDIR /app

# Copy file requirements và cài đặt thư viện Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy mã Python vào container
COPY main.py .

# Chạy script main.py khi container khởi động
CMD ["python", "main.py"]
