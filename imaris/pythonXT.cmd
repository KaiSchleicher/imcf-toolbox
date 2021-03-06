@echo off

:: make changes to environment variables non-permanent
setlocal enableextensions

:: NOTE: "%~1" is "%1" with surrounding quotes removed
if "%~1"=="" (goto :no_imsver)
set IMSVER=%~1
set IMSPATH=C:\Program Files\Bitplane\Imaris %IMSVER%

echo Setting PYTHONPATH for XT interface.
set PYTHONPATH=%IMSPATH%\XT\python\private;%IMSPATH%\XT\python;%IMSPATH%;%PYTHONPATH%

:: adjusting the PATH is required so the necessary DLLs will be found:
::  - bzip2.dll
::  - ice34.dll
::  - iceutil34.dll
::  - slice34.dll
set PATH=%IMSPATH%;%PATH%




echo Starting Python for ImarisXT %IMSVER%.
title IP[y]:XT
C:\Python27\python.exe
goto :clean_exit

:no_imsver
echo.
echo ERROR: no Imaris version specified!
echo.
echo EXAMPLE: %0 "x64 7.7.1"
echo.

:clean_exit
endlocal