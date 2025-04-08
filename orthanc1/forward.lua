docker-compose restart orthanc1-- Danh sách các Orthanc Peers để chuyển tiếp. Nếu để trống, danh sách sẽ được tải động khi Orthanc khởi động.
local PEER_LIST = {}

-- Hàm callback được gọi khi có sự thay đổi trong Orthanc
function OnChange(changeType, level, resourceId)
    -- Khi Orthanc khởi động
    if changeType == ChangeType.ORTHANC_STARTED then
        if #PEER_LIST == 0 then
            -- Lấy danh sách các peer từ REST API
            local response = RestApiGet('/peers/')
            PEER_LIST = ParseJson(response)
            Orthanc.LogInfo('Danh sách Peer: ' .. DumpJson(PEER_LIST))
        end
    end

    -- Khi một study trở nên ổn định
    if changeType == ChangeType.STABLE_STUDY then
        Orthanc.LogInfo('Study ổn định: ' .. resourceId)
        for _, peer in ipairs(PEER_LIST) do
            -- Gửi study đến từng peer
            local requestBody = {
                Asynchronous = false,
                Compress = true,
                Permissive = true,
                Priority = 0,
                Resources = { resourceId },
                Synchronous = false
            }
            local response, errorMessage = RestApiPost('/peers/' .. peer .. '/store', DumpJson(requestBody))
            if response then
                Orthanc.LogInfo('Study ' .. resourceId .. ' đã được chuyển tiếp đến peer ' .. peer)
            else
                Orthanc.LogError('Không thể chuyển tiếp study ' .. resourceId .. ' đến peer ' .. peer .. ': ' .. errorMessage)
            end
        end
    end
end

-- Đăng ký callback
RegisterOnChangeCallback(OnChange)

-- Hàm được gọi khi một instance DICOM được lưu trữ trong Orthanc
function OnStoredInstance(instanceId, tags, metadata)
    Orthanc.LogInfo("Instance được lưu trữ: " .. instanceId)

    -- Tên của modality đích (phải khớp với cấu hình trong "DicomModalities")
    local destination = "PACS2"

    -- Gửi instance đến modality đích
    local success, errorMessage = Orthanc.SendToModality(destination, instanceId)

    -- Kiểm tra kết quả gửi
    if success then
        Orthanc.LogInfo("Instance " .. instanceId .. " đã được chuyển tiếp thành công đến " .. destination)
    else
        Orthanc.LogError("Không thể chuyển tiếp instance " .. instanceId .. " đến " .. destination .. ": " .. errorMessage)
    end
end