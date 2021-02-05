from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import xml.etree.ElementTree as ET
import os
import time
from pprint import pprint
import glob
import unidecode
from progressbar import ProgressBar
from progressbar import FormatLabel
from progressbar import Percentage
from progressbar import Bar
from progressbar import RotatingMarker
from progressbar import ETA

def datos_marca_inpi(driver, parametros, log, inputfile=None, tmpdir=os.getcwd()):

    def _get_acta_data(acta_a_buscar):


        url = parametros["url"]
        url = url.replace("{ACTA}", acta_a_buscar)

        #log.info("connect to: {0}".format(url))
        driver.get(url)

        tipo = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, parametros["tipo_marca_xpath"]))
        )
        denominacion = driver.find_element_by_xpath(parametros["denominacion_xpath"])
        time.sleep(1)
        return [
            unidecode.unidecode(acta_a_buscar),
            tipo.text,
            denominacion.text
        ]

    datos = [('Acta', 'Tipo', 'Denominacion')]
    with open(inputfile, "r") as f:
        actas = f.readlines()

    widgets = [FormatLabel(''), ' ', Percentage(), ' ', Bar('#'), ' ', ETA(), ' ', RotatingMarker()]
    bar = ProgressBar(widgets=widgets, maxval=len(actas))

    i = 1
    for acta_a_buscar in actas:
        acta_a_buscar = acta_a_buscar.strip()
        datos.append(_get_acta_data(acta_a_buscar))
        widgets[0] = FormatLabel('[Acta: {0}]'.format(acta_a_buscar))
        bar.update(i)
        i = i + 1
    bar.finish()

    driver.quit()

    return datos