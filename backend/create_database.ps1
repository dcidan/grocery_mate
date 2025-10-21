Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "COMPLETE DATABASE FIX FOR GROCERY-MATE" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""

# Step 1: Stop everything
Write-Host "Step 1: Stopping all containers..." -ForegroundColor Yellow
docker-compose down 2>&1 | Out-Null
Start-Sleep -Seconds 2
Write-Host "  ✅ Containers stopped" -ForegroundColor Green
Write-Host ""

# Step 2: Start database
Write-Host "Step 2: Starting database container..." -ForegroundColor Yellow
docker-compose up -d
Start-Sleep -Seconds 10
Write-Host "  ✅ Container started" -ForegroundColor Green
Write-Host ""

# Step 3: Create database directly
Write-Host "Step 3: Creating grocery_db database..." -ForegroundColor Yellow
Write-Host "  Executing SQL command in container..." -ForegroundColor Gray

$sqlCommand = @"
SELECT 'CREATE DATABASE grocery_db ENCODING ''UTF8''' 
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'grocery_db')\gexec
"@

$result = docker exec grocery_postgres psql -U grocery_user -d postgres -c "$sqlCommand" 2>&1

Write-Host "  ✅ Database command executed" -ForegroundColor Green
Write-Host ""

# Step 4: Verify database exists
Write-Host "Step 4: Verifying database..." -ForegroundColor Yellow

$dbList = docker exec grocery_postgres psql -U grocery_user -d postgres -c "\l" 2>&1 | Select-String "grocery_db"

if ($dbList) {
    Write-Host "  ✅ CONFIRMED: grocery_db exists!" -ForegroundColor Green
    Write-Host "  Database info: $dbList" -ForegroundColor Gray
} else {
    Write-Host "  ⚠️  Could not confirm via \l command, trying alternative..." -ForegroundColor Yellow
    
    # Try to connect directly
    $testConnect = docker exec grocery_postgres psql -U grocery_user -d grocery_db -c "SELECT 1" 2>&1
    
    if ($testConnect -match "1 row") {
        Write-Host "  ✅ CONFIRMED: Can connect to grocery_db!" -ForegroundColor Green
    } else {
        Write-Host "  ❌ ERROR: Cannot confirm grocery_db exists" -ForegroundColor Red
        Write-Host "  Creating database manually..." -ForegroundColor Yellow
        
        docker exec grocery_postgres psql -U grocery_user -d postgres -c "CREATE DATABASE grocery_db ENCODING 'UTF8'" 2>&1 | Out-Null
        
        Write-Host "  ✅ Database created" -ForegroundColor Green
    }
}

Write-Host ""

# Step 5: Fix .env file in backend
Write-Host "Step 5: Creating clean .env file..." -ForegroundColor Yellow

Set-Location backend

$envContent = "DATABASE_URL=postgresql://grocery_user:grocery_pass@localhost:5432/grocery_db"

if (Test-Path .env) {
    Remove-Item .env -Force
}

# Create with UTF-8 encoding (no BOM)
[System.IO.File]::WriteAllText("$PWD\.env", $envContent, [System.Text.UTF8Encoding]::new($false))

Write-Host "  ✅ .env file created" -ForegroundColor Green
Write-Host "  Content: $envContent" -ForegroundColor Gray
Write-Host ""

# Step 6: Test connection from Python
Write-Host "Step 6: Testing Python connection..." -ForegroundColor Yellow

if (-not $env:VIRTUAL_ENV) {
    Write-Host "  Activating virtual environment..." -ForegroundColor Gray
    .\venv\Scripts\Activate.ps1
}

$testScript = @"
import sys
import os
os.environ['DATABASE_URL'] = 'postgresql://grocery_user:grocery_pass@localhost:5432/grocery_db'

try:
    from sqlalchemy import create_engine, text
    
    engine = create_engine(
        'postgresql://grocery_user:grocery_pass@localhost:5432/grocery_db',
        client_encoding='utf8'
    )
    
    with engine.connect() as conn:
        result = conn.execute(text('SELECT current_database()'))
        db_name = result.fetchone()[0]
        print(f'  ✅ Connected to database: {db_name}')
    
    engine.dispose()
    sys.exit(0)
except Exception as e:
    print(f'  ❌ Connection failed: {e}')
    sys.exit(1)
"@

python -c $testScript

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "=" * 70 -ForegroundColor Green
    Write-Host "✅ ALL FIXES COMPLETED SUCCESSFULLY!" -ForegroundColor Green
    Write-Host "=" * 70 -ForegroundColor Green
    Write-Host ""
    Write-Host "Database 'grocery_db' is ready and accessible from Python!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Now start your backend:" -ForegroundColor Yellow
    Write-Host "  cd backend" -ForegroundColor White
    Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor White
    Write-Host "  uvicorn app.main:app --reload" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "=" * 70 -ForegroundColor Red
    Write-Host "⚠️  FIX INCOMPLETE - PYTHON CONNECTION FAILED" -ForegroundColor Red
    Write-Host "=" * 70 -ForegroundColor Red
    Write-Host ""
    Write-Host "Database exists but Python cannot connect." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Please try starting backend anyway:" -ForegroundColor Yellow
    Write-Host "  uvicorn app.main:app --reload" -ForegroundColor White
    Write-Host ""
    Write-Host "If it fails, check:" -ForegroundColor Yellow
    Write-Host "  1. Docker is running: docker ps" -ForegroundColor White
    Write-Host "  2. Container logs: docker logs grocery_postgres" -ForegroundColor White
    Write-Host "  3. .env file exists in backend folder" -ForegroundColor White
}

Set-Location ..