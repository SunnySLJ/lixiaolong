# Planning with Files - 初始化脚本
# 用于快速创建规划文件

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Planning with Files - 初始化" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$projectRoot = Get-Location
$files = @(
    "task_plan.md",
    "findings.md", 
    "progress.md"
)

foreach ($file in $files) {
    $path = Join-Path $projectRoot $file
    if (Test-Path $path) {
        Write-Host "✓ $file (已存在)" -ForegroundColor Green
    } else {
        "# $file" | Out-File -FilePath $path -Encoding utf8
        Write-Host "✓ $file (已创建)" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "规划文件已就绪！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "下一步：" -ForegroundColor Yellow
Write-Host "1. 编辑 task_plan.md 定义任务目标" -ForegroundColor White
Write-Host "2. 开始执行任务" -ForegroundColor White
Write-Host "3. 在 progress.md 记录进展" -ForegroundColor White
Write-Host ""
