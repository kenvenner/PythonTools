@echo off
rem build out the python version environment
rem
rem default is 3.7
if "%1%" == "" (
   SET VERSION=7
) ELSE (
   echo here
   SET VERSION=%1%
)
rem
rem
if "%VERSION%" == "6" (
SET PGM=%USERPROFILE%\AppData\Local\Programs\Python\Python36\python.exe
)
if "%VERSION%" == "7" (
SET PGM=%USERPROFILE%\AppData\Local\Programs\Python\Python37\python.exe
)
if "%VERSION%" == "9" (
SET PGM=%USERPROFILE%\AppData\Local\Programs\Python\Python39\python.exe
)
if "%VERSION%" == "10" (
SET PGM=%USERPROFILE%\AppData\Local\Programs\Python\Python310\python.exe
)
rem
@echo off
if exist venv (
echo VENV already exists - no action required
goto exit
)
@echo on
if not exist venv (
%PGM% -m venv venv
call venv\scripts\activate
python -m pip install --upgrade pip
pip install wheel
)
:exit
