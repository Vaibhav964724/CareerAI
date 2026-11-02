# Start CareerAI Backend with automatic port 8000 cleanup
Set-Location -Path "$PSScriptRoot\backend"

# 1. Clean up port 8000 if in use
$conn = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue
if ($conn) {
    Write-Host "[CareerAI] Releasing busy port 8000..." -ForegroundColor Yellow
    $conn | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }
    Start-Sleep -Milliseconds 500
}

# 2. Activate virtual environment
if (Test-Path ".\venv\Scripts\Activate.ps1") {
    .\venv\Scripts\Activate.ps1
}

# 3. Start Uvicorn
Write-Host "[CareerAI] Starting FastAPI Backend on http://127.0.0.1:8000..." -ForegroundColor Green
python -m uvicorn app.main:app --reload --port 8000
