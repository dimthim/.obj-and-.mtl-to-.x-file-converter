@echo off
c:
cd ..\..\..\..\..\..\..\..\..\..\..\..\..\..
cd PythonProjects\FileConverter\TempFiles
dir/b> ..\ConvertMe.txt
cd  .. 
py FileConverter.py
cd ConvertedFiles
MOVE *.x x:\3dGame\Data
cd..
del /Q ConvertedFiles
del /Q TempFiles
del ConvertMe.txt
x:
