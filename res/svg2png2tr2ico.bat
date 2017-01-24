@echo off
set INKSCAPE_DIR=C:\Program Files\Inkscape
::set IMAGEMAGICK_DIR=C:\Program Files\Inkscape
set PATH=%INKSCAPE_DIR%;%PATH%

:: inkscape
:: without GUI
:: http://tavmjong.free.fr/INKSCAPE/MANUAL/html/CommandLine-Export.html

:: ImageMagick

:: Conversion with inkscape preserves font
inkscape.exe -z --file=%1 --export-png=%~n1.png  -h=64 -w=64 --export-area-page

:: Convert white pixels to transparent
imconvert.exe %~n1.png -transparent white  %~n1_tr.png

:: Convert transparent png to ico
imconvert.exe %~n1_tr.png -define icon:auto-resize=64,48,32,16 %~n1.ico


IF %ERRORLEVEL% NEQ 0 (
  pause
)