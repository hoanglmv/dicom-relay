-- forward.lua

-- Danh sách các Orthanc Peers để chuyển tiếp. Nếu để trống, danh sách sẽ được tải động khi Orthanc khởi động.
local PEER_LIST = {}

-- Hàm được gọi khi có sự thay đổi trong Orthanc (study/stable, khởi động, v.v.)
function OnChange(changeType, level, resourceId)
  if changeType == ChangeType.ORTHANC_STARTED then
    if #PEER_LIST == 0 then
      local response = RestApiGet('/peers/')
      PEER_LIST = ParseJson(response)
      Orthanc.LogInfo('Danh sách Peer: ' .. DumpJson(PEER_LIST))
    end
  elseif changeType == ChangeType.STABLE_STUDY then
    Orthanc.LogInfo('Study ổn định: ' .. resourceId)
    for _, peer in ipairs(PEER_LIST) do
      local body = {
        Asynchronous = false,
        Compress     = true,
        Permissive   = true,
        Priority     = 0,
        Resources    = { resourceId },
        Synchronous  = false
      }
      local resp, err = RestApiPost('/peers/' .. peer .. '/store', DumpJson(body))
      if resp then
        Orthanc.LogInfo('Study ' .. resourceId .. ' đã được chuyển tiếp đến peer ' .. peer)
      else
        Orthanc.LogError('Không thể chuyển tiếp study ' .. resourceId .. ' đến peer ' .. peer .. ': ' .. err)
      end
    end
  end
end

-- Hàm được gọi khi một instance DICOM được lưu trữ
function OnStoredInstance(instanceId, tags, metadata)
  Orthanc.LogInfo("Instance được lưu trữ: " .. instanceId)

  local destination = "PACS2"
  local success, err = Orthanc.SendToModality(destination, instanceId)
  if success then
    Orthanc.LogInfo("Instance " .. instanceId .. " đã được chuyển tiếp thành công đến " .. destination)
  else
    Orthanc.LogError("Không thể chuyển tiếp instance " .. instanceId .. " đến " .. destination .. ": " .. err)
  end
end
