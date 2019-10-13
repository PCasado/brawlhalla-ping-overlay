# Brawlhalla Ping Overlay
## Build
### Requirements
* Python3.5 or newer
* latest PyInstaller
* Win32Api packages
### Steps
To build this source, execute `build.bat` or run:
```
  python3 -m PyInstaller --add-data="config.ini;README.PLEASE.txt" --distpath brawlhalla-ping-overlay --onefile brawlhalla-ping-overlay.py
```
Then copy `config.ini` and `README.PLEASE.txt` to `dist\` directory.