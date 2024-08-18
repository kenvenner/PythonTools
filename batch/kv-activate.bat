@echo off
rem build out the python version environment for venv
rem
rem
rem drop box is different so create unique environment
SET VUNIQUE=lt
rem
rem set directory
SET VENVDIR=venv
rem
rem default is 3.11
if "%1%" == "" (
   SET VERSION=11
) ELSE (
   echo here
   SET VERSION=%1%
)
rem
rem pick the version of python
if "%VERSION%" == "7" (
SET PGM=%USERPROFILE%\AppData\Local\Programs\Python\Python37\python.exe
SET VENVDIR=venv07
)
if "%VERSION%" == "9" (
SET PGM=%USERPROFILE%\AppData\Local\Programs\Python\Python39\python.exe
SET VENVDIR=venv09
)
if "%VERSION%" == "10" (
SET PGM=%USERPROFILE%\AppData\Local\Programs\Python\Python310\python.exe
SET VENVDIR=venv10
)
if "%VERSION%" == "11" (
SET PGM=%USERPROFILE%\AppData\Local\Programs\Python\Python311\python.exe
SET VENVDIR=venv11
)
if "%VERSION%" == "12" (
SET PGM=%USERPROFILE%\AppData\Local\Programs\Python\Python312\python.exe
SET VENVDIR=venv12
)
if "%VERSION%" == "13" (
SET PGM=%USERPROFILE%\AppData\Local\Programs\Python\Python313\python.exe
SET VENVDIR=venv13
)
if "%VERSION%" == "14" (
SET PGM=%USERPROFILE%\AppData\Local\Programs\Python\Python314\python.exe
SET VENVDIR=venv14
)
if "%VERSION%" == "15" (
SET PGM=%USERPROFILE%\AppData\Local\Programs\Python\Python315\python.exe
SET VENVDIR=venv15
)
rem
rem
rem Make the directory unique
SET VENVDIR=%VENVDIR%%VUNIQUE%
rem
rem
rem turn on local environment for python if machine supports it
rem
if "%computername%" == "KVENNER-X1" goto validmachine
if "%computername%" == "KVENNER-LENOVO1" goto validmachine
if "%computername%" == "DT-WIN11" goto validmachine

echo This computer not setup for venv
goto end

:validmachine
echo Python activate running %VENVDIR%\scripts\activate
call %VENVDIR%\scripts\activate
echo|set /p="Running python version: "
python -V

:end
