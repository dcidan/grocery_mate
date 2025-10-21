Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "STARTING GROCERYMATE BACKEND" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host ""

# Set UTF-8 encoding environment variables
$env:PYTHONIOENCODING = "utf-8"
$env:PGCLIENTENCODING = "UTF8"
$env:LC_ALL = "en_US.UTF-8"
$env:LANG = "en_US.UTF-8"

Write-Host "Environment variables set:" -ForegroundColor Yellow
Write-Host "  PYTHONIOENCODING = utf-8" -ForegroundColor Gray
Write-Host "  PGCLIENTENCODING = UTF8" -ForegroundColor Gray
Write-Host ""

# Activate virtual environment if not already activated
if (-not $env:VIRTUAL_ENV) {
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    .\venv\Scripts\Activate.ps1
    Write-Host "  ✅ Virtual environment activated" -ForegroundColor Green
    Write-Host ""
}

# Verify database exists
Write-Host "Checking database connection..." -ForegroundColor Yellow
$dbCheck = docker exec grocery_postgres psql -U grocery_user -d grocery_db -c "SELECT 1" 2>&1

if ($dbCheck -match "1 row") {
    Write-Host "  ✅ Database connection verified" -ForegroundColor Green
} else {
    Write-Host "  ⚠️  Could not verify database, but continuing..." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=" * 60 -ForegroundColor Green
Write-Host "Starting Uvicorn server..." -ForegroundColor Green
Write-Host "=" * 60 -ForegroundColor Green
Write-Host ""

# Start uvicorn with UTF-8 encoding
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000