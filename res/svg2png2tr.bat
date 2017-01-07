@echo off

:: inkscape
:: without GUI
:: http://tavmjong.free.fr/INKSCAPE/MANUAL/html/CommandLine-Export.html

:: ImageMagick

:: Conversion with inkscape preserves font
inkscape.exe -z --file=%1 --export-png=%~n1.png --export-area-page

:: Convert white pixels to transparent
imconvert.exe %~n1.png -transparent white  %~n1_tr.png


IF %ERRORLEVEL% NEQ 0 (
  pause
)