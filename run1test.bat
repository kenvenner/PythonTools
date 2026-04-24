@echo off
rem utility to simplify the command line setting for executing a single test
rem in a unittest oriented file
rem
rem define the test file we are working with (.py) file
SET PYFILE=t_kvexcel
rem
rem define the test class in this file we are working with
SET CLASS=TestUpdateExcelCells
rem
rem define the name of the test case we are working with and running
rem last line in this list will be the test that runs
SET TEST=test_update_excel_cells_p01_basic
SET TEST=test_update_excel_cells_p02_detects_already_open_workbook
rem
rem now run this single test
@echo on
python -m unittest %PYFILE%.%CLASS%.%TEST%
:eof
