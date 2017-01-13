@echo off

::**************************************************************************

SET /P FIRST=BUILD BINARY DISTRIBUTION WITH DLLs (Py2EXE)  (Y/[N])?
IF /I "%FIRST%" NEQ "Y" GOTO END
echo .

for %%i in (res/*.ui) do  (
							pyside-uic res/%%~ni.ui -o ui_%%~ni.py
							echo PySide-UIC processed %%~ni
)

pyside-rcc.exe  mainwindow.qrc -o mainwindow_rc.py

::http://www.py2exe.org/index.cgi/FAQ
:: py2exe additional argument is appended internally in the script
python setup.py

:END
echo .
endlocal

::**************************************************************************

SET /P SECOND=BUILD INSTALLER PACKAGE (Inno Setup) (Y/[N])?
IF /I "%SECOND%" NEQ "Y" GOTO END
echo .

::http://www.jrsoftware.org/ishelp/index.php?topic=compilercmdline
iscc /Qp InstallScript.iss

robocopy Output . *.exe  /NFL /NDL /NJH /NJS /nc /ns /np

:END
echo .
endlocal

::**************************************************************************

SET /P THIRD=CLEAN BUILD FILES (Y/[N])?
IF /I "%THIRD%" NEQ "Y" GOTO END
echo .

:: clean
RMDIR Output /S /Q
RMDIR dist /S /Q
RMDIR build /S /Q
del mainwindow_rc.py /Q
::del mainwindow_rc.pyc /F /Q

:END
echo .
endlocal

::**************************************************************************

pause