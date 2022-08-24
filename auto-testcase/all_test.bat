@echo off
setlocal ENABLEEXTENSIONS

rem - init(result report init..)
cmd /c init.bat

rem - all testcase (.py) run
FOR /F "tokens=* delims=|" %%i IN ('dir /b *.py') do (
echo.
echo [ %%i start ]
python -u %%i
echo [ %%i end ]
echo.
)

pause