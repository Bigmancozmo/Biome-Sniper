@echo off

echo Installing modules...
echo.
py -m pip uninstall discord.py
py -m pip install -r requirements.txt
echo.
echo Done! Starting program...
echo.
py gui.pyw