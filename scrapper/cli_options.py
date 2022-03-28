import gettext
from gettext import gettext as _
gettext.textdomain('scrapper')
def _my_gettext(s):
    """Traducir algunas cadenas de argparse."""
    current_dict = {'usage: ': 'uso: ',
                    'optional arguments': 'argumentos opcionales',
                    'show this help message and exit': 'mostrar esta ayuda y salir',
                    'positional arguments': 'argumentos posicionales',
                    'the following arguments are required: %s': 'los siguientes argumentos son requeridos: %s'}

    if s in current_dict:
        return current_dict[s]
    return s

gettext.gettext = _my_gettext

import argparse

from scrapper.__version__  import __version__
from scrapper.__version__  import NAME
from scrapper.__version__  import DESCRIPTION
from scrapper.__version__  import URL
from scrapper.__version__  import AUTHOR
from scrapper.__version__  import EMAIL
from scrapper.__version__  import VERSION
from scrapper.__version__  import COPYRIGHT



def init_argparse():
    """Inicializar parametros del programa."""
    cmdparser = argparse.ArgumentParser(prog=NAME,
                                        description="%s\n%s\n" % (DESCRIPTION, COPYRIGHT),
                                        epilog="",
                                        add_help=True,
                                        formatter_class=make_wide(argparse.HelpFormatter, w=80, h=48)
    )

    opciones = {    "data": {
                                "type": str,
                                "nargs": '?',
                                "action": "store",
                                 "default": "",
                                "help": _("Datos a capturar")
                    },
                    "--version -v": {
                                "action":    "version",
                                "version":    VERSION,
                                "help":        _("Mostrar el número de versión y salir")
                    },
                    "--show-data -s": {
                                "action":    "store_true",
                                "dest":        "showdata",
                                "default":    False,
                                "help":        _("Mostrar los datos a capturar disponibles")
                    },
                    "--output-path -o": {
                                "type":     str,
                                "action":   "store",
                                "dest":     "outputpath",
                                "default":   ".",
                                "help":       _("Carpeta de outputh de los datos capturados")
                    },
                    "--output-file -f": {
                                "type":     str,
                                "action":   "store",
                                "dest":     "outputfile",
                                "default":    None,
                                "help":        _("Nombre del archivo de output de los datos capturados")
                    },
                    "--input-file -i": {
                                "type":     str,
                                "action":   "store",
                                "dest":     "inputfile",
                                "default":   None,
                                "help":      _("Nombre del archivo de entrada de datos")
                    },
                    "--output-type -t": {
                                "type":     str,
                                "action":   "store",
                                "dest":     "outputtype",
                                "default":  "None",
                                "help":     _("Formato de salida")
                    },
                    "--log-level -n": {
                                "type":     str,
                                "action":   "store",
                                "dest":     "loglevel",
                                "default":  "info",
                                "help":     _("Nivel de log")
                    },
                    "--log-file -l": {
                            "type":	str,
                            "action": "store",
                            "dest":	"logfile",
                            "default": None,
                            "help":	_("Archivo de log"),
                            "metavar": "file"
                    },
                    "--quiet -q": {
                                "action":     "store_true",
                                "dest":     "quiet",
                                "default":    False,
                                "help":        _("Modo silencioso sin mostrar absolutamente nada.")
                    },
                     "--show-browser -b": {
                                "action":   "store_true",
                                "dest":     "show_browser",
                                "default":  False,
                                "help":     _("Muestra el navegador y la interacción")
                    },
                    "--input-param -p": {
                                "type":     str,
                                "action":   "store",
                                "dest":     "inputparam",
                                "default":   None,
                                "help":      _("Parametro variable de entrada")
                    },
            }

    for key, val in opciones.items():
        args = key.split()
        kwargs = {}
        kwargs.update(val)
        cmdparser.add_argument(*args, **kwargs)

    return cmdparser



def make_wide(formatter, w=120, h=40):
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