import os
import pydicom
import numpy as np
import cv2
from pydicom.dataset import Dataset, FileDataset
import datetime
import time
import uuid

def convert_png_to_dicom(png_path, output_dicom_path, patient_name="Test^Patient", patient_id="123456"):
    # Đọc ảnh PNG
    img = cv2.imread(png_path, cv2.IMREAD_GRAYSCALE)  # DICOM thường là grayscale
    if img is None:
        raise ValueError(f"Không thể đọc ảnh: {png_path}")
    
    # Lấy kích thước ảnh
    rows, cols = img.shape

    # Tạo DICOM dataset
    file_meta = pydicom.dataset.FileMetaDataset()
    file_meta.MediaStorageSOPClassUID = pydicom.uid.generate_uid()
    file_meta.MediaStorageSOPInstanceUID = pydicom.uid.generate_uid()
    file_meta.ImplementationClassUID = "1.2.826.0.1.3680043.10.543"

    ds = FileDataset(output_dicom_path, {}, file_meta=file_meta, preamble=b"\0" * 128)

    # Thông tin thời gian
    dt = datetime.datetime.now()
    ds.ContentDate = dt.strftime("%Y%m%d")
    ds.ContentTime = dt.strftime("%H%M%S.%f")

    # Các tag cơ bản
    ds.PatientName = patient_name
    ds.PatientID = patient_id
    ds.StudyInstanceUID = str(uuid.uuid4())
    ds.SeriesInstanceUID = str(uuid.uuid4())
    ds.SOPInstanceUID = file_meta.MediaStorageSOPInstanceUID
    ds.Modality = "CT"
    ds.StudyDate = dt.strftime("%Y%m%d")
    ds.SeriesNumber = "1"
    ds.InstanceNumber = "1"

    # Kích thước ảnh
    ds.Rows = rows
    ds.Columns = cols
    ds.SamplesPerPixel = 1
    ds.PhotometricInterpretation = "MONOCHROME2"
    ds.BitsAllocated = 8
    ds.BitsStored = 8
    ds.HighBit = 7
    ds.PixelRepresentation = 0

    # Gán dữ liệu ảnh
    ds.PixelData = img.tobytes()

    # Lưu file DICOM
    ds.save_as(output_dicom_path)
    print(f"Đã lưu: {output_dicom_path}")

# Ví dụ chuyển nhiều ảnh
input_folder = "dicom_dir"
output_folder = "output"

os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if filename.endswith(".png"):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename.replace(".png", ".dcm"))
        convert_png_to_dicom(input_path, output_path)
