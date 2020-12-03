from struct import calcsize
from struct import pack
from struct import unpack
import logging
import tempfile
import os
import sys
import re
import subprocess
import warnings


def expand_filename(filename):
    """expand_filename: Expansión de un path con keywords

    Args:
        filename (str): Path completo a un archivo con keywords

    Example:
        >>> expand_filename("{Desktop}")
    """

    replace_paths = {
        '{desktop}': os.path.join(os.path.expanduser('~'), 'Desktop'),
        '{tmpdir}': tempfile.gettempdir(),
        '{tmpfile}': tempfile.mktemp()
    }

    for path_keyword in replace_paths:
        if path_keyword in filename:
            filename.replace(path_keyword, replace_paths[path_keyword]())

    return filename


def loginfo(msg, printmsg=False):
    if printmsg:
        print(msg)
    logging.info(msg.replace("|", " "))


def logerror(msg):
    logging.error(msg.replace("|", " "))


def resource_path(relative):
    """Obtiene un path, toma en consideración el uso de pyinstaller"""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)


def make_wide(formatter, w=120, h=36):
    """Return a wider HelpFormatter, if possible."""
    try:
        # https://stackoverflow.com/a/5464440
        # beware: "Only the name of this class is considered a public API."
        kwargs = {'width': w, 'max_help_position': h}
        formatter(None, **kwargs)
        return lambda prog: formatter(prog, **kwargs)
    except TypeError:
        warnings.warn("argparse help formatter failed, falling back.")
        return formatter

def normalizefn(text, delim='-'):
    """Normaliza una cadena para ser usada como nombre de archivo.

    Args:
        text (str): String a normalizar
        delim (str): Caracter de reemplazo de aquellos no vÃ¡lidos

    Ejemplo:
        >>> from openerm.Utils import *
        >>> Start downloading file("Esto, no es vÃ¡lido como nombre de Archivo!", "-")
        'esto-no-es-valido-como-nombre-de-archivo'
    """
    result = []
    for word in _punct_re.split(text):
        word = normalize('NFKD', word).encode('ascii', 'ignore')
        word = word.decode('utf-8')
        if word:
            result.append(word)
    return delim.join(result)




