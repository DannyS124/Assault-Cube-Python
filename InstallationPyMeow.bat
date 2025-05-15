@echo off
setlocal ENABLEEXTENSIONS

:: Ask user for Python path
echo Please copy and paste the full path to your Python executable (e.g., D:\Python312-32\python.exe)
set /p PYTHON_PATH=Python Path: 

:: Ask user for pyMeow path
echo Please copy and paste the full path to the pyMeow directory (e.g., C:\Users\danny\OneDrive\Desktop\pyMeow-1.73.42)
set /p PYMEOW_PATH=pyMeow Directory: 

:: Validate Python executable
if not exist "%PYTHON_PATH%" (
    echo [ERROR] Invalid Python path provided.
    pause
    exit /b
)

:: Validate pyMeow directory
if not exist "%PYMEOW_PATH%" (
    echo [ERROR] Invalid pyMeow directory path.
    pause
    exit /b
)

:: Ensure pip and wheel are available
echo Installing wheel package if not present...
"%PYTHON_PATH%" -m pip install --upgrade pip
"%PYTHON_PATH%" -m pip install wheel

:: Check if pyMeow is already installed
echo Checking for existing pyMeow installation...
"%PYTHON_PATH%" -m pip show pyMeow >nul 2>&1
if %errorlevel%==0 (
    echo pyMeow is already installed. Attempting to uninstall first...
    "%PYTHON_PATH%" -m pip uninstall -y pyMeow
)

:: Navigate to pyMeow directory
cd /d "%PYMEOW_PATH%"
if errorlevel 1 (
    echo [ERROR] Could not change directory to %PYMEOW_PATH%.
    pause
    exit /b
)

:: Install pyMeow using pip
echo Installing pyMeow...
"%PYTHON_PATH%" -m pip install .

:: Verify installation
echo Verifying the installation...
"%PYTHON_PATH%" -m pip show pyMeow >nul 2>&1
if %errorlevel%==0 (
    echo pyMeow successfully installed!

    echo Running pyMeow test...
    "%PYTHON_PATH%" -c "import pyMeow; print('pyMeow is working properly:', dir(pyMeow))"
) else (
    echo [ERROR] pyMeow installation failed.
    pause
    exit /b
)

echo Done. Press any key to exit.
pause >nul
endlocal
