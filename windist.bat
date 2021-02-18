@echo off

REM --------------------------------------------------------
REM Bat para la generación del paquete de deploy de scrapper
REM --------------------------------------------------------


REM --------------------------------------------------------
REM Creación del paquete para distribuir
REM --------------------------------------------------------
@echo --------------------------------------------------------
@echo Generando distribucion con scrapper..
@echo --------------------------------------------------------
@pyinstaller scrapper\cli.py --onedir --noupx --clean --noconfirm -n scrapper --paths=scrapper

@echo --------------------------------------------------------
@echo Copiando archivos y herramientas adicionales..
@echo --------------------------------------------------------

REM --------------------------------------------------------
REM Ini de la applicación
REM !! Copiar manualmente si es necesario
REM --------------------------------------------------------
REM @copy scrapper\scrapper.cfg dist\scrapper\scrapper.cfg

REM --------------------------------------------------------
REM Eliminar archivos de trabajo
REM --------------------------------------------------------
@echo --------------------------------------------------------
@echo Eliminando archivos de trabajo ..
@echo --------------------------------------------------------
@rmdir build /S /Q
@del *.spec /S /F /Q

@echo --------------------------------------------------------
@echo Carpeta a distribuir dist\pboletin..
@echo --------------------------------------------------------
