Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "FIXING UNICODE/ENCODING ISSUES - COMPLETE" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host ""

Write-Host "This script will:" -ForegroundColor Yellow
Write-Host "  1. Stop any running backend servers" -ForegroundColor Gray
Write-Host "  2. Update database.py with UTF-8 encoding" -ForegroundColor Gray
Write-Host "  3. Update init_db.py with UTF-8 encoding" -ForegroundColor Gray
Write-Host "  4. Recreate .env file with proper encoding" -ForegroundColor Gray
Write-Host "  5. Test database connection" -ForegroundColor Gray
Write-Host ""

# Step 1: Update database.py
Write-Host "Step 1: Updating app/database.py..." -ForegroundColor Yellow

$databaseContent = @'
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://grocery_user:grocery_pass@localhost:5432/grocery_db"
)

# Create engine with explicit UTF-8 encoding
engine = create_engine(
    DATABASE_URL,
    client_encoding='utf8',
    connect_args={
        'options': '-c client_encoding=utf8'
    }
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
'@

[System.IO.File]::WriteAllText("$PWD\app\database.py", $databaseContent, [System.Text.UTF8Encoding]::new($false))
Write-Host "  ✅ database.py updated" -ForegroundColor Green

# Step 2: Clean .env file
Write-Host ""
Write-Host "Step 2: Creating clean .env file..." -ForegroundColor Yellow

$envContent = "DATABASE_URL=postgresql://grocery_user:grocery_pass@localhost:5432/grocery_db"

if (Test-Path .env) {
    Remove-Item .env -Force
}

[System.IO.File]::WriteAllText("$PWD\.env", $envContent, [System.Text.UTF8Encoding]::new($false))
Write-Host "  ✅ .env file recreated with UTF-8 encoding" -ForegroundColor Green

# Step 3: Restart database
Write-Host ""
Write-Host "Step 3: Restarting database container..." -ForegroundColor Yellow
Set-Location ..
docker-compose restart 2>&1 | Out-Null
Start-Sleep -Seconds 5
Set-Location backend
Write-Host "  ✅ Database restarted" -ForegroundColor Green

# Step 4: Test connection
Write-Host ""
Write-Host "Step 4: Testing database connection..." -ForegroundColor Yellow

if (-not $env:VIRTUAL_ENV) {
    .\venv\Scripts\Activate.ps1
}

python -c @"
import psycopg2
try:
    conn = psycopg2.connect(
        host='localhost',
        port=5432,
        database='postgres',
        user='grocery_user',
        password='grocery_pass',
        client_encoding='utf8'
    )
    print('  ✅ Connection successful')
    conn.close()
except Exception as e:
    print(f'  ❌ Connection failed: {e}')
    exit(1)
"@

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "=" * 60 -ForegroundColor Green
    Write-Host "✅ ALL FIXES APPLIED SUCCESSFULLY" -ForegroundColor Green
    Write-Host "=" * 60 -ForegroundColor Green
    Write-Host ""
    Write-Host "Now start the backend:" -ForegroundColor Yellow
    Write-Host "  uvicorn app.main:app --reload" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "=" * 60 -ForegroundColor Red
    Write-Host "❌ CONNECTION TEST FAILED" -ForegroundColor Red
    Write-Host "=" * 60 -ForegroundColor Red
    Write-Host ""
    Write-Host "Please check:" -ForegroundColor Yellow
    Write-Host "  1. Docker Desktop is running" -ForegroundColor White
    Write-Host "  2. Database container is running: docker ps" -ForegroundColor White
    Write-Host "  3. Restart database: docker-compose restart" -ForegroundColor White
}