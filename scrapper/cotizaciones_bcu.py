from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import xml.etree.ElementTree as ET
import os
import time
from pprint import pprint


def cotizaciones_bcu(driver, parametros, tmpdir = os.getcwd()):

    print("Conectandose con la página")
    driver.get(parametros["url"])

    print("Seleccionamos todas las monedas")
    element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, parametros["boton_xpath"]))
    )
    element.click()

    print("Descargamos el xml")
    element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, parametros["xml_xpath"]))
    )
    element.click()
    time.sleep(10)
    driver.quit()


    print("Procesamos los datos")
    # Lectura del archivo descargado
    import glob
    # print(download_folder)
    datos = [('Fecha', 'ISO', 'Nombre', 'TCC', 'TCV', 'Arb')]
    for file in glob.glob("{0}/Cotizaciones*.xml".format(tmpdir)):

        absolute_file_name = os.path.join(tmpdir, file)
        tree = ET.parse(absolute_file_name)
        root = tree.getroot()
        # print([fecha.text for fecha in root.findall(".//*")])
        datos.extend(list(zip(
            [e.text for e in root.findall(".//{Cotiza}Fecha")],
            [e.text for e in root.findall(".//{Cotiza}CodigoISO")],
            [e.text for e in root.findall(".//{Cotiza}Nombre")],
            [e.text for e in root.findall(".//{Cotiza}TCC")],
            [e.text for e in root.findall(".//{Cotiza}TCV")],
            [e.text for e in root.findall(".//{Cotiza}ArbAct")]
        )))
        os.remove(absolute_file_name)

    return datos