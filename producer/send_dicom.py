import requests
import sys

def send_dicom(file_path):
    url = "http://localhost:8042/instances"
    headers = {"Content-Type": "application/dicom"}
    with open(file_path, "rb") as f:
        data = f.read()
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        print("Successfully sent DICOM file.")
    else:
        print("Failed to send DICOM file. Status code:", response.status_code)
        print(response.text)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python send_dicom.py <dicom_file>")
        sys.exit(1)
    file_path = sys.argv[1]
    send_dicom(file_path)
