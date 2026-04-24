@echo off
rem run all tests and output the results into a log file
@echo on
call t_all > test_all.log 2>&1
@echo off
ech Please review [test_all.log] for test results
:eof
