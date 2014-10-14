set path=C:\Python27;C:\Python27\Scripts
python ftp.py
@echo off
echo %path%
if %errorlevel%==9009 (
	echo Downloading Dependancies...
	cscript install\download-dependancies.vbs
	msiexec /i install\python-2.7.8.msi
	set path=C:\Python27;C:\Python27\Scripts
	python install\get-pip.py
	easy_install install\pycrypto-2.6.win32-py2.7.exe
	pip install paramiko
	python ftp.py
)

