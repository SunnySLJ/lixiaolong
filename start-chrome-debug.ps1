# 启动带远程调试端口的 Chrome
$chromePath = "C:\Program Files\Google\Chrome\Application\chrome.exe"
$debugPort = 18800
$userDataDir = "C:\Users\爽爽\AppData\Local\Google\Chrome\User Data"

# 检查 Chrome 是否已经在运行
$existingChrome = Get-Process chrome -ErrorAction SilentlyContinue | Where-Object { $_.Path -eq $chromePath }

if ($existingChrome) {
    Write-Host "Chrome 已在运行，尝试关闭..."
    $existingChrome | Stop-Process -Force
    Start-Sleep -Seconds 2
}

Write-Host "正在启动带远程调试端口的 Chrome..."
Start-Process $chromePath -ArgumentList "--remote-debugging-port=$debugPort", "--user-data-dir=`"$userDataDir`"", "--no-first-run", "--disable-gpu"

Start-Sleep -Seconds 5
Write-Host "✓ Chrome 已启动，调试端口：$debugPort"
