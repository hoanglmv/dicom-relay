from pydicom import dcmread
from pynetdicom import AE, StoragePresentationContexts, build_context
from pynetdicom.sop_class import CTImageStorage
import os

# Cấu hình Orthanc1
ORTHANC1_AET = "ORTHANC1"  # AET của Orthanc1 (phải khớp với cấu hình trong Orthanc1.json)
ORTHANC1_HOST = "localhost"  # Địa chỉ của Orthanc1
ORTHANC1_PORT = 4242  # Cổng DICOM của Orthanc1

# Đường dẫn file DICOM
DICOM_FILE_PATH = r"D:\vhproj\dicom-relay\dicom_dir\ID_0089_AGE_0071_CONTRAST_0_CT.dcm"  # Thay bằng đường dẫn file DICOM của bạn

def send_dicom_to_orthanc1(dicom_file):
    # Kiểm tra file DICOM có tồn tại không
    if not os.path.exists(dicom_file):
        print(f"❌ File DICOM không tồn tại: {dicom_file}")
        return False

    # Đọc file DICOM
    ds = dcmread(dicom_file)
    print(f"📂 Đang gửi file DICOM: {dicom_file}")
    print(f"🩺 Patient Name: {ds.PatientName}, Study ID: {ds.StudyID}")

    # Khởi tạo Application Entity (AE)
    ae = AE()

    # Thêm Presentation Context cho CT Image Storage (hoặc các SOP Class khác nếu cần)
    ae.add_requested_context(CTImageStorage)

    # Kết nối đến Orthanc1
    assoc = ae.associate(ORTHANC1_HOST, ORTHANC1_PORT, ae_title=ORTHANC1_AET)
    if assoc.is_established:
        print(f"✅ Kết nối thành công đến Orthanc1 ({ORTHANC1_HOST}:{ORTHANC1_PORT})")

        # Gửi file DICOM
        status = assoc.send_c_store(ds)

        # Kiểm tra trạng thái gửi
        if status:
            print(f"✅ Gửi file DICOM thành công! Status: {status.Status}")
        else:
            print("❌ Gửi file DICOM thất bại!")

        # Đóng kết nối
        assoc.release()
        print("🔌 Đã đóng kết nối với Orthanc1.")
        return True
    else:
        print(f"❌ Không thể kết nối đến Orthanc1 ({ORTHANC1_HOST}:{ORTHANC1_PORT})")
        return False

if __name__ == "__main__":
    success = send_dicom_to_orthanc1(DICOM_FILE_PATH)
    if success:
        print("✨ File DICOM đã được gửi đến Orthanc1. Kiểm tra Orthanc2 để xác nhận auto-forward.")
    else:
        print("⚠️ Có lỗi xảy ra khi gửi file DICOM.")