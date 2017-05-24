:: Output IP address of default gateway to upload to file
ipconfig | "%gnu%\grep" "Default Gateway" | "%gnu%\mawk" "{print $NF}" > "%server%"

:: Retrieve IP address of default gateway from file
set /p ip=<"%server%"

:: Delete output file
del "%server%"

:: Upload stuff to nginx server
set "desktop=%USERPROFILE%\Desktop"
cd %desktop%\windows-analyzer
C:\Python27\python.exe finish.py %ip%
