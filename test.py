import requests
import time

# Đường dẫn file DICOM
dicom_filepath = r"C:\Users\firek\Downloads\archive (1)\dicom_dir\ID_0095_AGE_0071_CONTRAST_0_CT.dcm"

# URL API của Orthanc1 để upload file
upload_url = "http://localhost:8042/instances"
headers_upload = {"Content-Type": "application/dicom"}

# Upload file lên Orthanc1
with open(dicom_filepath, "rb") as f:
    response = requests.post(upload_url, headers=headers_upload, data=f)

response.raise_for_status()
upload_result = response.json()
instance_id = upload_result["ID"]
print("✅ Upload thành công! Instance ID:", instance_id)

# Chờ 5-10 giây để AutoForward thực hiện
time.sleep(10)

# Kiểm tra trên Orthanc2 xem file đã được forward hay chưa
orthanc2_url = "http://localhost:8043/instances"
response2 = requests.get(orthanc2_url)
response2.raise_for_status()
instances_orthanc2 = response2.json()
print("📂 Danh sách Instance trên Orthanc2:", instances_orthanc2)

# Kiểm tra xem instance_id đã được chuyển hay chưa
if instance_id in instances_orthanc2:
    print("✅ Auto-forward thành công! File đã có trên Orthanc2.")
else:
    print("⚠️ Chưa tìm thấy file trên Orthanc2. Kiểm tra logs của Orthanc1 để debug.")
