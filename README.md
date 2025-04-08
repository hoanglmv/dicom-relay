# 1. Tạo mạng Docker bridge
docker network create dicom-network

# 2. Chạy các container và gán vào mạng
docker run -d \
  --name orthanc1 \
  --network dicom-network \
  -p 8042:8042 \
  -p 4242:4242 \
  jodogne/orthanc

docker run -d \
  --name orthanc2 \
  --network dicom-network \
  -p 8043:8042 \
  -p 4243:4242 \
  jodogne/orthanc