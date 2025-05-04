# watcher/main.py
import time
import requests
import logging
import os

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')

ORTHANC_URL = "http://research_pacs:8042"
DICOM_DIR = "/app/dcm"
# Tạo thư mục lưu trữ nếu chưa tồn tại
os.makedirs(DICOM_DIR, exist_ok=True)

# Tập hợp các ID đã biết
known_ids = set()

logging.info("Watcher started, polling Orthanc for new instances...")

while True:
    try:
        # Lấy danh sách instance IDs từ Orthanc
        resp = requests.get(f"{ORTHANC_URL}/instances")
        resp.raise_for_status()
        instance_ids = resp.json()
        
        # Kiểm tra ID mới
        for inst_id in instance_ids:
            if inst_id not in known_ids:
                logging.info(f"Found new DICOM instance: {inst_id}")
                # Tải file DICOM về
                file_resp = requests.get(f"{ORTHANC_URL}/instances/{inst_id}/file")
                if file_resp.status_code == 200:
                    filepath = os.path.join(DICOM_DIR, f"{inst_id}.dcm")
                    with open(filepath, 'wb') as f:
                        f.write(file_resp.content)
                    logging.info(f"Downloaded DICOM file to {filepath}")
                else:
                    logging.warning(f"Failed to download instance {inst_id}: HTTP {file_resp.status_code}")
                known_ids.add(inst_id)
    except requests.RequestException as e:
        logging.error(f"Error connecting to Orthanc: {e}")
    
    time.sleep(5)  # đợi 5 giây trước khi kiểm tra lại
