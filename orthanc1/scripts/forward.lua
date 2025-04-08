function OnStoredInstance(instanceId, tags, metadata)
  -- Kiểm tra xem Lua script có được thực thi không
  Orthanc.LogInfo("Lua script executed for instance: " .. instanceId)

  -- Gửi tệp DICOM đến Orthanc2
  local modality = "PACS2" -- Tên modality đã cấu hình trong orthanc1.json
  local success, err = Orthanc.SendToModality(modality, instanceId)

  if success then
    Orthanc.LogInfo("Successfully forwarded instance " .. instanceId .. " to " .. modality)
  else
    Orthanc.LogError("Failed to forward instance " .. instanceId .. " to " .. modality .. ": " .. err)
  end
end
