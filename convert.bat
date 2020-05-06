@echo off
X:
cd \3dGame\misc\TempFiles
dir/b> ..\ConvertMe.txt
cd ..
py FileConverter.py
del /Q Tempfiles
del ConvertMe.txt