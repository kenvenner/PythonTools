rem this takes you to the folder where code is maintained locally
rem on machine dt-win8
rem
if "%computername%" == "DT-WIN8" (
    @echo on
    c:
    cd \users\public\documents\code
)
ELSE (
    @echo on
    c:
    cd %USERPROFILE%\Dropbox\LinuxShare\python
)
    
