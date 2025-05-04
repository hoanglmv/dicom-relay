import time
import requests

def main():
    base_url = 'http://hospital_pacs:8042'  # URL của Orthanc HOSPITAL-PACS trong Docker Compose
    processed = set()  # lưu các instance đã forward để không lặp lại

    while True:
        try:
            # Gọi API GET /instances để lấy danh sách instance hiện có
            response = requests.get(f"{base_url}/instances")
            response.raise_for_status()
            instance_ids = response.json()  # danh sách ID của các instance
        except Exception as e:
            print(f"[ERROR] Không thể lấy danh sách instances: {e}")
            time.sleep(5)
            continue

        # Forward từng instance mới (chưa xử lý) sang RESEARCH-PACS
        for instance_id in instance_ids:
            if instance_id not in processed:
                try:
                    url = f"{base_url}/modalities/RESEARCH-PACS/store"
                    payload = {"Resources": [instance_id]}
                    # Gửi POST request: gửi instance qua peer "RESEARCH-PACS"
                    resp = requests.post(url, json=payload)
                    resp.raise_for_status()
                    print(f"[INFO] Đã forward instance {instance_id} sang RESEARCH-PACS")
                    processed.add(instance_id)
                except Exception as e:
                    print(f"[ERROR] Lỗi khi forward instance {instance_id}: {e}")
        # Chờ vài giây trước khi vòng lặp tiếp
        time.sleep(5)

if __name__ == "__main__":
    main()
