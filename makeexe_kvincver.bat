@echo off
rem - save all changes prior to changing the build version of the file
git commit -a
rem - update the build variable and commit this single change
kvincver --buildonly kv_incver.py
git commit -m "new compilation build version" kv_incver.py
rem - copy the file to the version we want
copy kv_incver.py kvincver.py
rem - digital signature - 2026-04-24;kv not working at this time - so rem'd out - this is setup
SET CMDFILE=kvincver
SET ADDCMD=
rem
SET CERTFILE="C:\Users\ken\OneDrive - e-Share\code\cert\Digicert-20201207 (1).pfx"
SET CERTPWD=<put_the_pwd_here_when_you_want_to_sign>
rem
SET SIGNEXE="c:\Program Files (x86)\Windows Kits\10\bin\x64\signtool.exe"
SET TIMEURL= http://timestamp.digicert.com
rem
SET PYFILE=%CMDFILE%.py
SET EXEFILE=".\dist\%CMDFILE%.exe"
rem - compile into a single file EXE this tool - kvincver.exe
@echo on
pyinstaller %PYFILE% --onefile %ADDCMD%
@echo off
rem - if digital signature worked - we would run the command line to digitally sign this EXE
rem %SIGNEXE% sign /f %CERTFILE% /t %TIMEURL%  /p %CERTPWD% %EXEFILE%
rem
@ech on
rem run this exe to validate it works
%EXEFILE% --help
rem
rem copy this to locations it needs to go
copy %EXEFILE% C:\bin
copy %EXEFILE% ..\..\SoftwareInstalls
:eof
