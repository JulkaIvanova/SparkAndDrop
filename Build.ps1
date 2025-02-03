$path = $MyInvocation.MyCommand.Path | split-path -parent
C:\Users\Þëÿ\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\Scripts\pyinstaller --onefile --noconsole --icon=$path\data\icon.png $path\startWindow.py
pause