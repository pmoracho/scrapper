from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import xml.etree.ElementTree as ET
import os
import time
from pprint import pprint
import glob

from progressbar import ProgressBar, Percentage, Bar, ETA, RotatingMarker, FormatLabel


def zonaprop(driver, parametros, log, inputfile=None, tmpdir=os.getcwd(), inputparam=None):

    def _get_element(xpath):
        try:
            return driver.find_element_by_xpath(xpath).text
        except Exception:
            return ""

    def _get_dat_from_ul(xpath):
        try:
            d = {
                "ambientes": None,
                "baños": None,
                "antiguedad": None,
                "superficie": None,
                "superficie_cubierta": None,
                "cochera": "No",
                "toilette": "No",
            }

            ul = driver.find_element_by_xpath(xpath)
            for text in [el.text for el in ul.find_elements_by_tag_name("li")]:
                if "Ambientes" in text:
                    d["ambientes"] = text.split(" ")[0]
                if "Baños" in text:
                    d["baños"] = text.split(" ")[0]
                if "Antigüedad" in text:
                    d["antiguedad"] = text.split(" ")[0]
                if "Total" in text:
                    d["superficie"] = text.split(" ")[0]
                if "Cubierta" in text:
                    d["superficie_cubierta"] = text.split(" ")[0]
                if "Cochera" in text:
                    d["cochera"] = "Si"
                if "Toilette" in text:
                    d["toilette"] = "Si"
            return d

        except Exception:
            return []

    def _get_propiedad_data(url_propiedad):

        driver.get(url_propiedad)

        precio = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, parametros["precio_xpath"]))
        )
        tipo_op = _get_element(parametros["price_type"])
        expensas = "'" + _get_element(parametros["expensas_xpath"])
        decripcion = _get_element(parametros["descripcion_xpath"])

        datos = _get_dat_from_ul(parametros["datos_ul_xpath"])
        mts_totales = datos["superficie"]
        mts_cubiertos = datos["superficie_cubierta"]
        ambientes = datos["ambientes"]
        baños = datos["baños"]
        cochera = datos["cochera"]
        toilette = datos["toilette"]
        antiguedad = datos["antiguedad"]

        direccion = _get_element(parametros["dir_xpath"])
        publicado = _get_element(parametros["publicado_xpath"])
        inmobiliaria = _get_element(parametros["inmobiliaria_xpath"])

        return (
            decripcion,
            direccion.replace('\r', '').replace('\n', '').replace('Ver en mapa', ''),
            precio.text,
            expensas,
            mts_totales,
            mts_cubiertos,
            ambientes,
            baños,
            toilette,
            cochera,
            antiguedad,
            publicado,
            inmobiliaria,
            url_propiedad,
        )

    datos = [('Detalle', 'Dirección', 'Precio', 'Expensas', 'Mts Totales', 'Mts Cubiertos', 'Ambientes', 'Baños', 'Toilette', 'Cochera',
            'Antiguedad', 'Publicado', 'Inmobiliaria', 'URL')]

    urls = list()

    if inputparam is not None:
        urls = [inputparam]
    else:
        with open(inputfile, "r") as f:
            urls = f.readlines()

    widgets = [FormatLabel(''), ' ', Percentage(), ' ', Bar('#'), ' ', ETA(), ' ', RotatingMarker()]
    bar = ProgressBar(widgets=widgets, maxval=len(urls))

    i = 1
    for url_propiedad in urls:
        url_propiedad = url_propiedad.strip()

        try:
            # a = 1/0
            datos.append(_get_propiedad_data(url_propiedad))
        except Exception as err:

            vacio = list("" for _ in range(len(datos[0])))
            vacio[-1] = "!!!Error: {0}".format(err)
            datos.append(tuple(vacio))

        widgets[0] = FormatLabel('[Prop: {0}]'.format(url_propiedad))
        bar.update(i)
        i = i + 1

    bar.finish()

    driver.quit()

    return datos

