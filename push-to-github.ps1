# GitHub 推送脚本
# 使用方法：在 PowerShell 中运行 .\push-to-github.ps1

Write-Host "===================================="
Write-Host "BOSS 直聘自动投递 - 推送到 GitHub"
Write-Host "===================================="
Write-Host ""

$repoUrl = "https://github.com/chenlibulei/boss-auto-apply.git"
$token = "YOUR_GITHUB_TOKEN_HERE"  # 替换为你的 Personal Access Token

Write-Host "仓库地址：$repoUrl"
Write-Host ""

# 设置 Git 凭据
$env:GIT_ASKPASS = "echo"
$env:GIT_USERNAME = "chenlibulei"
$env:GIT_PASSWORD = $token

Write-Host "正在推送代码到 GitHub..."
Write-Host ""

# 推送
git push -u origin main --force

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "====================================" -ForegroundColor Green
    Write-Host "✅ 推送成功！" -ForegroundColor Green
    Write-Host "====================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "访问仓库：https://github.com/chenlibulei/boss-auto-apply"
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "====================================" -ForegroundColor Red
    Write-Host "❌ 推送失败" -ForegroundColor Red
    Write-Host "====================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "请检查："
    Write-Host "1. 网络连接是否正常"
    Write-Host "2. Token 是否有效"
    Write-Host "3. 仓库是否存在"
    Write-Host ""
    Write-Host "如果仓库不存在，请先在 GitHub 创建："
    Write-Host "https://github.com/new"
    Write-Host ""
}
