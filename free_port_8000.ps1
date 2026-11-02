# Utility script to free port 8000 if a dangling Python/Uvicorn process holds it
Write-Host "Checking for processes listening on port 8000..." -ForegroundColor Cyan

$connections = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue

if ($connections) {
    foreach ($conn in $connections) {
        $pidToKill = $conn.OwningProcess
        $proc = Get-Process -Id $pidToKill -ErrorAction SilentlyContinue
        Write-Host "Found process holding port 8000: PID $pidToKill ($($proc.ProcessName))" -ForegroundColor Yellow
        Stop-Process -Id $pidToKill -Force -ErrorAction SilentlyContinue
        Write-Host "Successfully terminated PID $pidToKill." -ForegroundColor Green
    }
    Write-Host "Port 8000 is now free!" -ForegroundColor Green
} else {
    Write-Host "Port 8000 is already free. No action needed." -ForegroundColor Green
}
