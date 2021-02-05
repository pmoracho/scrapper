@echo off

@echo --------------------------------------------------------
@echo Creación del paquete para distribuir
@echo--------------------------------------------------------
@pyinstaller scrapper\cli.py --onedir --noupx --clean --noconfirm -n scrapper

@echo --------------------------------------------------------
@echo Copiando archivos y herramientas adicionales..
@echo --------------------------------------------------------
@copy scrapper.cfg dist\scrapper\scrapper.cfg

@echo --------------------------------------------------------
@echo Eliminando archivos de trabajo ..
@echo --------------------------------------------------------
@rmdir build /S /Q
@del *.spec /S /F /Q

@echo --------------------------------------------------------
@echo Descarga del chrome driver versión 88..
@echo --------------------------------------------------------
@curl https://chromedriver.storage.googleapis.com/88.0.4324.96/chromedriver_win32.zip --output chromedriver_win32.zip

@echo --------------------------------------------------------
@echo Descomprimir chromedriver_win32.zip en la carpeta
@echo ./dist/scrapper
@echo
@echo NOTA: https://chromedriver.chromium.org/downloads
@echo --------------------------------------------------------
