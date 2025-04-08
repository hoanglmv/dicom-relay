-- Hàm được gọi khi một instance DICOM được lưu trữ trong Orthanc2
function OnStoredInstance(instanceId, tags, metadata)
    -- Log thông tin về instance mới được lưu trữ
    Orthanc.LogInfo("📥 Instance mới được lưu trữ trên Orthanc2: " .. instanceId)

    -- In thêm thông tin chi tiết (nếu cần)
    if tags.PatientName then
        Orthanc.LogInfo("🩺 Tên bệnh nhân: " .. tags.PatientName)
    end
    if tags.StudyDescription then
        Orthanc.LogInfo("📄 Mô tả study: " .. tags.StudyDescription)
    end
end