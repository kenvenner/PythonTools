@echo off
rem utility to simplify the command line setting for executing a single test
rem in a unittest oriented file
rem
rem define the test file we are working with (.py) file
SET PYFILE=t_copy_comments
rem
rem define the test class in this file we are working with
SET CLASS=TestCopyComment
rem
rem define the name of the test case we are working with and running
rem last line in this list will be the test that runs
SET TEST=
SET TEST=test_src_to_dst_actions_p04_internal_copy_fields
rem
rem now run this single test
@echo on
python -m unittest %PYFILE%.%CLASS%.%TEST%
:eof
