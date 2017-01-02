@echo off
:: Using ImageMagick

imconvert %1 -define icon:auto-resize=64,48,32,16 %~n1.ico



:: Batch process
rem for %%i in (*.svg) do  (
rem 							convert %%~ni.svg -define icon:auto-resize=64,48,32,16 %%~ni.ico
rem 							echo Converted %%~ni
rem )

REM pause