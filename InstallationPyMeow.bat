@echo off
setlocal

REM Prompt user for Python path and pyMeow path
echo Please copy and paste the full path to your Python executable (e.g., D:\Python312-32\python.exe)
set /p PYTHON_PATH=Python Path: 
echo Please copy and paste the full path to the pyMeow directory (e.g., C:\Users\danny\OneDrive\Desktop\pyMeow-1.73.42)
set /p PYMEOW_PATH=pyMeow Directory: 

REM Check if the provided Python path is valid
if not exist "%PYTHON_PATH%" (
    echo Invalid Python path provided. Please check the path and try again.
    pause
    exit /b
)

REM Check if the provided pyMeow directory path is valid
if not exist "%PYMEOW_PATH%" (
    echo Invalid pyMeow directory path provided. Please check the path and try again.
    pause
    exit /b
)

REM Install wheel package
echo Installing wheel package...
%PYTHON_PATH% -m pip install wheel

REM Navigate to the pyMeow directory
echo Navigating to the pyMeow directory...
cd /d %PYMEOW_PATH%

REM Install pyMeow using setup.py
echo Installing pyMeow...
%PYTHON_PATH% setup.py install

REM Verify the installation
echo Verifying the installation...
%PYTHON_PATH% -m pip list | findstr pyMeow

REM Done
echo Installation complete. Press any key to exit.
pause >nul

endlocal





