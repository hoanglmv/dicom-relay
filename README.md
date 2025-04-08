README: Triển khai Orthanc với Docker & Auto-Forward DICOM

🚀 Giới thiệu

Dự án này sử dụng Docker để chạy hai container Orthanc (Orthanc1 và Orthanc2) với khả năng tự động chuyển tiếp (auto-forward) file DICOM từ Orthanc1 sang Orthanc2.

📌 Yêu cầu hệ thống

Docker & Docker Compose

Python 3.x (để chạy script upload)

🔧 1. Cài đặt và chạy Docker

1.1. Build và chạy container

Chạy lệnh sau trong thư mục chứa docker-compose.yml:

docker-compose up -d --build

📌 Giải thích:

up -d: Chạy các container dưới nền.

--build: Build lại image nếu cần thiết.

1.2. Kiểm tra container đang chạy

docker ps

Kết quả mong đợi:

CONTAINER ID   IMAGE       COMMAND                  PORTS                    NAMES
abc12345       orthanc1    "/entrypoint.sh"        0.0.0.0:8042->8042/tcp   orthanc1
xyz67890       orthanc2    "/entrypoint.sh"        0.0.0.0:8043->8043/tcp   orthanc2

1.3. Kiểm tra logs của Orthanc1

docker logs orthanc1 --tail 50

🌐 2. Thêm container vào mạng Docker thủ công

Kiểm tra danh sách mạng Docker:

docker network ls

Thêm orthanc1 và orthanc2 vào mạng dicom-network nếu chưa có:

docker network connect dicom-network orthanc1
docker network connect dicom-network orthanc2

Kiểm tra lại:

docker network inspect dicom-network

📤 3. Upload file DICOM bằng upload.py

3.1. Cài đặt thư viện cần thiết

pip install requests

3.2. Chạy script upload

python upload.py <path_to_dicom_file>

📌 Ví dụ:

python upload.py C:/Users/firek/Downloads/dicom_dir/ID_0095_AGE_0071_CONTRAST_0_CT.dcm

Sau khi upload thành công, Orthanc1 sẽ tự động chuyển file sang Orthanc2.

3.3. Kiểm tra file trên Orthanc2

curl -X GET http://localhost:8043/instances

Nếu file xuất hiện, quá trình auto-forward đã hoạt động chính xác. Nếu không, kiểm tra log của Orthanc1:

docker logs orthanc1 --tail 50

🔄 4. Cập nhật file DICOM

Nếu bạn muốn cập nhật lại file, chỉ cần chạy lại script upload:

python upload.py <path_to_new_dicom_file>

📌 Debugging

Nếu file không tự động forward, kiểm tra log của Orthanc1 bằng lệnh:

docker logs orthanc1 --tail 50

Nếu Orthanc2 không nhận được file, kiểm tra Orthanc2 có nhận đúng file không:

curl -X GET http://localhost:8043/instances

Nếu cần gửi file thủ công từ Orthanc1 đến Orthanc2, dùng lệnh:

curl -X POST -H "Content-Type: application/json" -d "[\"<instance_id>\"]" http://localhost:8042/modalities/PACS2/store

✅ Kết luận

Dự án này giúp bạn tự động forward file DICOM giữa hai server Orthanc. Nếu gặp lỗi, hãy kiểm tra log của Orthanc1 và Orthanc2. Chúc bạn thành công! 🚀

