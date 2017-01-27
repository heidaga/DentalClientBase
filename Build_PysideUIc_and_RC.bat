@echo off

rem del ui_mainwindow.py* /q

for %%i in (res/*.ui) do  (
							pyside-uic res/%%~ni.ui -o ui_%%~ni.py
							echo PySide-UIC processed %%~ni
)

rem del mainwindow_rc.py* /q
pyside-rcc.exe  mainwindow.qrc -o mainwindow_rc.py
::pyrcc4.exe  mainwindow.qrc -o mainwindow_rc.py

::python DentalClientBaseGUI.py
::pause