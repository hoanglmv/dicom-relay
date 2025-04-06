import requests
import time
import os

# Orthanc2 REST API được expose tại cổng 8043 (theo cấu hình docker-compose)
ORTHANC2_URL = "http://localhost:8043"
DOWNLOAD_FOLDER = "downloaded"

def get_instances():
    url = f"{ORTHANC2_URL}/instances"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()  # danh sách instance IDs
    else:
        print("Error fetching instances:", response.status_code)
        return []

def download_instance(instance_id):
    url = f"{ORTHANC2_URL}/instances/{instance_id}/file"
    response = requests.get(url)
    if response.status_code == 200:
        file_path = os.path.join(DOWNLOAD_FOLDER, f"{instance_id}.dcm")
        with open(file_path, "wb") as f:
            f.write(response.content)
        print(f"Downloaded instance {instance_id} to {file_path}")
        # Tại đây bạn có thể tích hợp bài toán domain xử lý file
    else:
        print(f"Error downloading instance {instance_id}: {response.status_code}")

def main():
    if not os.path.exists(DOWNLOAD_FOLDER):
        os.makedirs(DOWNLOAD_FOLDER)

    processed = set()

    while True:
        instances = get_instances()
        for instance_id in instances:
            if instance_id not in processed:
                download_instance(instance_id)
                processed.add(instance_id)
        time.sleep(10)

if __name__ == "__main__":
    main()
