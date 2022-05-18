@echo off
rem This file calls the python program to pull git branches
rem that are local and create a file that will delete them
rem
@echo on
cd "%USERPROFILE%\OneDrive - e-Share\code\eshare-scripts"
python git-branch-delete.py > ken.bat
@echo off
echo edit ken.bat to clean it up and
echo run ken.bat to cause the delete take place
