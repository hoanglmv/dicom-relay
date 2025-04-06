function OnStoredInstance(instanceId, tags, metadata)
    Orthanc.Log("Forwarding instance: " .. instanceId)
    
    -- Lấy nội dung của instance vừa lưu
    local instance = RestApiGet("/instances/" .. instanceId)
    
    -- Địa chỉ của Orthanc2 (lưu ý: từ container Orthanc1, tên service theo docker-compose là "orthanc2")
    local forwardUrl = "http://orthanc2:8042/instances"
    
    -- Gửi file DICOM đến Orthanc2
    local response = RestApiPost(forwardUrl, instance)
    
    if response == nil then
      Orthanc.Log("Failed to forward instance: " .. instanceId)
    else
      Orthanc.Log("Successfully forwarded instance: " .. instanceId)
    end
  end
  