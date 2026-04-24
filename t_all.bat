@echo off
rem - run all tests for library files
rem
@echo on
rem Std Utility Tests
python t_kvcsv.py
python t_kvdate.py
ptyhon t_kvexcel.py
python t_kvjpg.py
python t_kvlogger.py
python t_kvmatch.py
python t_kvutil.py
python t_kvxls.py
python t_kv_incver.py
rem python t_xlsx_diff.py
rem
rem Google Integration Tests
python t_kvgmail.py
python t_kvgmailrcv.py
python t_kvgmailsend.py
:eof
