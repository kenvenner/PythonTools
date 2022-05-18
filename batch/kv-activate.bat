@echo off
rem turn on local environment for python if machine supports it
rem
if "%computername%" == "KVENNER-X1" (
   @echo on
   call venv\scripts\activate
)
