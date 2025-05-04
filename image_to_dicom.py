import pydicom
from pydicom.dataset import Dataset, FileDataset
from pydicom.uid import generate_uid, ExplicitVRLittleEndian
import numpy as np
from PIL import Image
import datetime
import os

def image2dicom(png_path, dicom_path, patient_id="CT001", study_id="STUDY001"):
    # Đọc ảnh PNG và chuyển sang mảng numpy
    image = Image.open(png_path).convert("L")  # Grayscale
    pixel_array = np.array(image)

    dt = datetime.datetime.now()
    current_time = dt.strftime("%H%M%S")
    current_date = dt.strftime("%Y%m%d")

    # khởi tạo 1 file meta information cho một file dicom => ĐỌc thêm về m
    file_meta = pydicom.Dataset() # Khởi tạo đối tượng Dataset trong file DICOM ( từ nhóm tag 0008 trở đi) chứa meta data và pixel data của hình ảnh, bao gồm nhiều module như Patient Module, Study Module, Series Module
    file_meta.MediaStorageSOPClassUID = pydicom.uid.SecondaryCaptureImageStorage # khởi tạo class UID
    file_meta.MediaStorageSOPInstanceUID = generate_uid() # Khởi tạo íntanceUID
    file_meta.ImplementationClassUID = generate_uid()

    ds = FileDataset(dicom_path, {}, file_meta=file_meta, preamble=b"\0" * 128)
    ds.is_little_endian = True
    ds.is_implicit_VR = False

    # Gán các tag cơ bản
    ds.SOPClassUID = file_meta.MediaStorageSOPClassUID
    ds.SOPInstanceUID = file_meta.MediaStorageSOPInstanceUID
    ds.StudyInstanceUID = generate_uid()
    ds.SeriesInstanceUID = generate_uid()
    ds.PatientID = patient_id
    ds.StudyID = study_id
    ds.Modality = "CT"
    ds.StudyDate = current_date
    ds.StudyTime = current_time

    # Lưu trữ dữ liệu ảnh
    ds.Rows, ds.Columns = pixel_array.shape
    ds.SamplesPerPixel = 1 # Ảnh độ xám
    ds.PhotometricInterpretation = "MONOCHROME2" # giá trị 0 là đen,255 là trắng
    ds.PixelRepresentation = 0
    ds.BitsAllocated = 8
    ds.BitsStored = 8
    ds.HighBit = 7
    ds.PixelData = pixel_array.tobytes()

    # Lưu file DICOM
    ds.save_as(dicom_path)
    print(f"✔️ Converted {png_path} to {dicom_path}")


image2dicom("/home/myvh/hoang/project/dicom-relay/Data/test/adenocarcinoma/000108 (3).png", "output/image.dcm")
