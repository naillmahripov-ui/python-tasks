@echo off
chcp 65001 >nul
set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1
set PY=%LOCALAPPDATA%\Programs\Python\Python313\python.exe
cd /d "%~dp0"
"%PY%" launcher.py
pause
