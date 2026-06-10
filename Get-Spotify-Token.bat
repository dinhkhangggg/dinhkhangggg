@echo off
setlocal
echo ==============================================
echo    TOOL LAY MA SPOTIFY REFRESH TOKEN
echo ==============================================
echo.
set /p CLIENT_ID="[1] Nhap Client ID cua ban: "
set /p CLIENT_SECRET="[2] Nhap Client Secret cua ban: "
echo.
echo Vao trinh duyet va mo duong link sau:
echo https://accounts.spotify.com/authorize?client_id=%CLIENT_ID%^&response_type=code^&redirect_uri=https://example.com/callback^&scope=user-read-currently-playing,user-read-recently-played
echo.
echo Dang nhap Spotify va bam Agree.
echo Trinh duyet se chuyen huong toi trang example.com (Bao loi khong sao ca).
echo Ban hay COPY doan ma o tren thanh dia chi, TU SAU CHU "code=" den het.
echo.
set /p CODE="[3] Nhap ma CODE ban vua copy (Khong bao gom chu code=): "
echo.
echo Dang lay Refresh Token...
echo.

powershell -Command "$base64AuthInfo = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes('%CLIENT_ID%:%CLIENT_SECRET%')); $headers = @{ Authorization = ('Basic {0}' -f $base64AuthInfo) }; $body = @{ grant_type = 'authorization_code'; code = '%CODE%'; redirect_uri = 'https://example.com/callback' }; try { [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; $response = Invoke-RestMethod -Uri 'https://accounts.spotify.com/api/token' -Method Post -Headers $headers -Body $body; Write-Host '======================================' -ForegroundColor Green; Write-Host 'THANH CONG! REFRESH TOKEN CUA BAN LA:' -ForegroundColor Yellow; Write-Host $response.refresh_token -ForegroundColor Cyan; Write-Host '======================================' -ForegroundColor Green; } catch { Write-Host 'Co loi xay ra! Vui long kiem tra lai cac ma vua nhap.' -ForegroundColor Red; Write-Host $_.Exception.Message }"

echo.
pause
