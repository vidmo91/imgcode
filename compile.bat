pyinstaller --onefile .\imgcode.py -c -i icon.ico
del ./build -Force -Recurse
del ./imgcode.spec -Force
del ./__pycache__ -Force -Recurse
del ./.git -Force -Recurse