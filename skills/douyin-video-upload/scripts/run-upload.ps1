param(
    [string]$Video = "C:\Users\爽爽\Desktop\图片\2.mp4",
    [string]$Cover = "C:\Users\爽爽\Desktop\图片\2.cover.jpg",
    [string]$Title = "春日随拍小片段｜城市日常记录",
    [string]$Desc = "今天随手记录一段生活片段，节奏轻松，画面干净，适合当作日常更新。",
    [string[]]$Tags = @("日常记录", "生活碎片", "随拍", "vlog"),
    [switch]$Publish,
    [int]$PublishWaitSeconds = 900,
    [switch]$Headless,
    [switch]$CloseBrowser
)

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$uploader = Join-Path $scriptDir "douyin_upload.py"

if (-not (Test-Path $uploader)) {
    throw "Uploader script not found: $uploader"
}

$argsList = @(
    $uploader
    "--video", $Video
    "--cover", $Cover
    "--title", $Title
    "--desc", $Desc
    "--publish-wait-seconds", "$PublishWaitSeconds"
)

if ($Tags -and $Tags.Count -gt 0) {
    $argsList += "--tags"
    $argsList += $Tags
}

if ($Publish) {
    $argsList += "--publish"
}

if ($Headless) {
    $argsList += "--headless"
}

if ($CloseBrowser) {
    $argsList += "--close-browser"
}

& python @argsList
exit $LASTEXITCODE
