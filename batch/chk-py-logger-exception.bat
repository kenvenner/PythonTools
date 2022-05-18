@echo off
rem look for properly structured logger statements
rem and output where they are not to exectations
rem
@echo on
del chklogger.tmp
grep -n logger *.py | grep "{}" >> chklogger.tmp
grep -n logger *.py | grep "u'" >> chklogger.tmp
grep -n logger *.py | grep -v "%" >> chklogger.tmp


grep -n Exception *.py | grep -v "u'" | grep format >> chklogger.tmp
grep -n Exception *.py | grep -v format | grep -v "pytest.raises(Exception)" | grep -v "except Exception" >> chklogger.tmp
grep -n Exception *.py | grep "+"  >> chklogger.tmp

grep -n foramt *.py >> chklogger.tmp

sort chklogger.tmp >chklogger.log
cls
type chklogger.log
