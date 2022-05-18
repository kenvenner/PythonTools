@echo off
rem calls the python program that causes the master branch to be pulled
rem and then steps through each local branch and merges with master to bring
rem it up to speed - if that branch is NOT a purely local branch
rem
@echo on
cd "%USERPROFILE%\OneDrive - e-Share\code\eshare-scripts"
python git-branch-merge.py > ken.bat
@echo off
echo run ken.bat to cause the merge take place
