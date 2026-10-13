@echo off
echo ===================================================
echo   FocusPika - Standalone Windows Executable Builder
echo ===================================================
echo.

set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python is not installed or not in PATH!
    pause
    exit /b 1
)

echo [1/4] Checking and installing dependencies...
python -m pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to install requirements!
    pause
    exit /b 1
)

echo [2/4] Running automated test suite with pytest...
python -m pytest tests/
if %ERRORLEVEL% NEQ 0 (
    echo [WARNING] Some tests failed, proceeding with caution...
)

echo [3/4] Packaging FocusPika with PyInstaller...
python -m PyInstaller FocusPika.spec --clean --noconfirm
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] PyInstaller build failed!
    pause
    exit /b 1
)

echo [4/4] Verifying standalone executable in dist/ ...
if exist "dist\FocusPika.exe" (
    echo.
    echo ===================================================
    echo   BUILD SUCCESSFUL!
    echo   Standalone executable created:
    echo   %SCRIPT_DIR%dist\FocusPika.exe
    echo ===================================================
) else (
    echo [ERROR] Could not find dist\FocusPika.exe!
    pause
    exit /b 1
)

echo.
pause
