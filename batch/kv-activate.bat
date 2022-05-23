@echo off
rem turn on local environment for python if machine supports it
rem
if "%computername%" == "KVENNER-X1" (
   echo Python activate running venv\scripts\activate
   @echo on
   call venv\scripts\activate
) ELSE (
   echo This computer not setup for venv
)
