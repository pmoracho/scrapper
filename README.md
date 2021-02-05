# scrapper

Un simple y sencillo scrapper de páginas mediante **Selenium**, medianamente
configurable y con, hasta ahora, dos rutinas básicas o modelos de captura.

* Cotizaciones del BCU
* Datos de Marcas publicadas en el INPI

# Instalación

## Requirimientos básicos:

Tener instalado y funcionando:

* Git
* Python 3.x

## 1. Entorno inicial básico

* Clonar repositorio
* Crear entorno virtual
* Activar entorno virtual
* actualizar `pip`
* Instalar requerimientos

```
git clone git@github.com:pmoracho/scrapper.git
cd scrapper
python -m venv .venv --prompt=scrapper
.venv\Scripts.activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 2. Despliegue

Para construir la carpeta de despliegue de la aplicación en Windows, en primer lugar, con eentorno activado, instalar [Pyinstaller][pyinstaller]:

    pip install pyinstaller

Luego simplemente ejecutar:

    windist.bat


La carpeta final con la herramienta y sus binarios es:

    scrapper\dist\scrapper

## Importante

Esta herramienta usa **Selenium** para la captura de las páginas, y además
requiere un driver de **chrome**, que básicamente es un navegador mínimo y
automatizable. Para que todo funcione correctamente, se debe descargar un driver
y copiarlo a la carpeta de despliegue. Tener en cuenta:

* [Descargar][chrome] el chrome driver consistente con la versión de Chrome del
  sistema
* Descomprimir el ejecutable en la carpeta de despliegue


[chrome]: https://chromedriver.chromium.org/downloads
[pyinstaller]: https://pyinstaller.readthedocs.io/en/stable/index.html#