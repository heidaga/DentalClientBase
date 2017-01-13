@echo off

pyrcc4.exe  mainwindow.qrc -o mainwindow_rc.py

::http://www.py2exe.org/index.cgi/FAQ
:: py2exe additional argument is appended internally in the script
python setup.py

::http://www.jrsoftware.org/ishelp/index.php?topic=compilercmdline
iscc /Qp InnoScript.iss

robocopy Output . *.exe  /NFL /NDL /NJH /NJS /nc /ns /np

:: clean
RMDIR Output /S /Q
RMDIR dist /S /Q
RMDIR build /S /Q
REM rem del mainwindow_rc.py /Q
::del mainwindow_rc.pyc /F /Q