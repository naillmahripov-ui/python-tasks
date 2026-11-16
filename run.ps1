param([Parameter(Mandatory=$true)][string]$File)

$env:PYTHONIOENCODING = "utf-8"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$python = Join-Path $env:LOCALAPPDATA "Programs\Python\Python313\python.exe"

if (-not (Test-Path $python)) {
    Write-Error "Python не найден: $python"
    exit 1
}

if (-not (Test-Path $File)) {
    Write-Error "Файл не найден: $File"
    exit 1
}

& $python $File
