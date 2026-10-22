@echo off
setlocal
cd /d "%~dp0"
echo.
echo PACE Anti-Cheat - Windows build helper
 echo This builds the desktop EXE locally; it does not run on GitHub Pages.
echo.
where py >nul 2>nul
if errorlevel 1 (
  echo Python launcher was not found.
  echo Install Python 3.11 or newer from https://www.python.org/downloads/windows/
  echo During installation, enable the option to add Python to PATH.
  pause
  exit /b 1
)
py -m pip install --upgrade pip pyinstaller
if errorlevel 1 goto :failed
if exist build rmdir /s /q build
if exist dist\PACE.exe del /q dist\PACE.exe
py -m PyInstaller --noconfirm --clean --onefile --windowed --name PACE --icon "app\assets\pace.ico" "app\pace_app.py"
if errorlevel 1 goto :failed
if not exist releases mkdir releases
for %%I in ("C:\Program Files (x86)\Inno Setup 6\ISCC.exe" "C:\Program Files\Inno Setup 6\ISCC.exe") do (
  if exist %%I (
    echo.
    echo Building the setup installer with Inno Setup...
    %%I "installer\PACE-Setup.iss"
    if errorlevel 1 goto :failed
    echo.
    echo Build complete. Check the releases folder for PACE-Setup-0.2.0-beta.exe
    goto :done
  )
)
echo.
echo PACE.exe was built in the dist folder.
echo To produce the custom installer, install Inno Setup 6 and rerun this file.
goto :done
:failed
echo.
echo Build failed. Read the error above, check Python and try again.
pause
exit /b 1
:done
pause
endlocal
