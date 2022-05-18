@echo off
rem compare that batch files in the current folders to those in the source
rem repo for bat files and show the differences
rem
SET OPTION=
if "%1" == "diff" (
    SET OPTION=--diff
)
python "%USERPROFILE%\OneDrive - e-Share\code\eshare-scripts\copy-file.py" . --src %USERPROFILE%\Dropbox\LinuxShare\python\tools\batch --ext bat --mtime %OPTION%
