# watcher/Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY main.py .
# Tạo thư mục lưu trữ DICOM
RUN mkdir -p /app/dcm
CMD ["python", "main.py"]
