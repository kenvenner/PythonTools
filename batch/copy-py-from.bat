@echo off
rem compare that python files in the current folders to those in the source
rem repo for bat files and show the differences
rem
rem
SET OPTION=
if "%1" == "diff" (
    SET OPTION=--diff
)
if "%1" == "winmerge" (
    SET OPTION=--winmerge
)
python "%USERPROFILE%\Dropbox\LinuxShare\python\tools\copy-file.py" . --src %USERPROFILE%\Dropbox\LinuxShare\python\tools --mtime %OPTION%
