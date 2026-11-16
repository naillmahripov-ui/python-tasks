@echo off
set PYW=%LOCALAPPDATA%\Programs\Python\Python313\pythonw.exe
cd /d "%~dp0"
start "" "%PYW%" server.py --open
