#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2014 Patricio Moracho <pmoracho@gmail.com>
#
# scrapper.py
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of version 3 of the GNU General Public License
# as published by the Free Software Foundation. A copy of this license should
# be included in the file GPL-3.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

"""
scrapper
========

Herramienta de línea de comandos para extracción de datos de páginas útiles

"""

try:
    import sys
    import gettext
    from gettext import gettext as _
    gettext.textdomain('scrapper')


    import codecs
    import re
    import os
    import logging
    import tempfile
    import time
    from urllib.parse import urlparse
    from configparser import ConfigParser
    import traceback

    from scrapper.drivers import get_chrome_driver
    from scrapper.models.cotizaciones_bcu import cotizaciones_bcu
    from scrapper.models.datos_marca_inpi import datos_marca_inpi
    from scrapper.models.zonaprop import zonaprop
    from scrapper.tabulate import tabulate
    from scrapper.cli_options import init_argparse
    from scrapper.__version__  import __version__
    from scrapper.__version__  import NAME
    from scrapper.__version__  import DESCRIPTION
    from scrapper.__version__  import URL
    from scrapper.__version__  import AUTHOR
    from scrapper.__version__  import EMAIL
    from scrapper.__version__  import VERSION

except ImportError as err:
    modulename = err.args[0].partition("'")[-1].rpartition("'")[0]
    print(_("No fue posible importar el modulo: %s") % modulename)
    sys.exit(-1)

_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.:]+')

class Log:

    def __init__(self, outputpath, loglevel, quiet = True):

        logging.basicConfig(filename=os.path.join(outputpath, 'scrapper.log'),
                            level=getattr(logging, loglevel.upper(), None),
                            format='%(asctime)s|%(levelname)s|%(message)s',
                            datefmt='%Y/%m/%d %I:%M:%S',
                            filemode='w')
        self.quiet = quiet


    def info(self, msg):

        if not self.quiet:
            print(msg)

        logging.info(msg.replace("|", " "))

    def error(self, msg):
        msg = "!!! Error ---> {0}".format(msg.replace("|", " "))
        if not self.quiet:
            print(msg)

        logging.error("Error: {0}".format(msg))


def show_data(available_data):

    tablestr = tabulate(
                    tabular_data        = available_data,
                    headers                = ["Data", "Descripción" ],
                    tablefmt            = "psql",
                    stralign            = "left",
                    override_cols_align = ["right", "left"]
        )

    print(tablestr)



class ProcessFlag():

    def __init__(self, data, outputpath):
        self.data = data
        self.outputpath = outputpath
        self._remove_files()

    def _remove_files(self):

        try:
            for status in ["ok", "error"]:
                filename = os.path.join(self.outputpath, "{}.{}".format(self.data, status))
                os.remove(filename)

        except FileNotFoundError:
            pass

    def flag(self, ok):

        filename = os.path.join(self.outputpath, "{}.{}".format(self.data, "ok" if ok else "error"))
        file = open(filename, 'w')
        file.close()

    def ok(self):
        self.flag(True)

    def error(self):
        self.flag(False)

def main():

    title = """
  ______    ______   _______    ______   _______   _______   ________  _______
 /      \  /      \ /       \  /      \ /       \ /       \ /        |/       \\
/$$$$$$  |/$$$$$$  |$$$$$$$  |/$$$$$$  |$$$$$$$  |$$$$$$$  |$$$$$$$$/ $$$$$$$  |
$$ \__$$/ $$ |  $$/ $$ |__$$ |$$ |__$$ |$$ |__$$ |$$ |__$$ |$$ |__    $$ |__$$ |
$$      \ $$ |      $$    $$< $$    $$ |$$    $$/ $$    $$/ $$    |   $$    $$<
 $$$$$$  |$$ |   __ $$$$$$$  |$$$$$$$$ |$$$$$$$/  $$$$$$$/  $$$$$/    $$$$$$$  |
/  \__$$ |$$ \__/  |$$ |  $$ |$$ |  $$ |$$ |      $$ |      $$ |_____ $$ |  $$ |
$$    $$/ $$    $$/ $$ |  $$ |$$ |  $$ |$$ |      $$ |      $$       |$$ |  $$ |
 $$$$$$/   $$$$$$/  $$/   $$/ $$/   $$/ $$/       $$/       $$$$$$$$/ $$/   $$/

{0} (v.{1})
{2}
"""

    cmdparser = init_argparse()

    try:
        args = cmdparser.parse_args()
        if not args.quiet:
            print(title.format(DESCRIPTION, VERSION, AUTHOR))
    except IOError as msg:
        args.error(str(msg))

    if args.outputpath:
        outputpath = args.outputpath
    else:
        outputpath = ''

    log = Log(outputpath=outputpath,
             loglevel=args.loglevel,
             quiet=args.quiet
    )
    log.info("Starting {0} - {1} (v{2})".format(NAME, DESCRIPTION, VERSION))

    # determine if application is a script file or frozen exe
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    elif __file__:
        application_path = os.path.dirname(__file__)

    cfgfile = os.path.join(application_path, '../scrapper.cfg')

    log.info("Loading config: {}".format(cfgfile))
    config = ConfigParser()

    # with open(os.path.join(os.path.dirname(__file__), 'scrapper.cfg')) as f:
    try:
        config.read_file(codecs.open(cfgfile, "r", "utf8"))
    except FileNotFoundError:

        errormsg = "No existe el archivo de configuración ({0})".format(cfgfile)
        print(errormsg)
        log.error(errormsg)
        sys.exit(-1)

    available_data = []

    for section_name in config.sections():

        if "data:" in section_name:
            data_id = section_name.split(":")[1]
            data_name = config[section_name]["name"]
            available_data.append((data_id, data_name))

    if args.showdata and available_data:
        show_data(available_data)
        sys.exit(0)

    if not args.data:
        log.error("scrapping model not specified")
        cmdparser.print_help()
        sys.exit(-1)

    datas = [p[0] for p in available_data if p[0] == args.data]
    if datas:
        data = datas[0]
        workpath = tempfile.mkdtemp()
        driver = get_chrome_driver(download_folder=workpath, show=args.show_browser)

        log.info("Data scrapping model: {}".format(data))

        section        = "data:" + data
        function_name  = config[section]["function"]

        if function_name in globals():
            function = globals()[function_name]
            log.info("calling: {}".format(function_name))
            start_time = time.time()
            try:
                datos = function(driver=driver,
                                log=log,
                                parametros=config[section],
                                inputfile=args.inputfile,
                                tmpdir=workpath,
                                inputparam=args.inputparam)

                driver.quit()
            except Exception:
                traceback.print_exc()

            elapsed_time = time.strftime('%H:%M:%S', time.gmtime(round(time.time() - start_time, 2)))

            n = len(datos) - 1
            if n > 0:

                registros = datos[1:]
                header_row = datos[0]

                if args.outputtype == "None":
                    registros = []
                    maxlen = len(max(header_row, key=len))
                    for r in datos[1:]:
                        for i, h in enumerate(header_row, 0):
                            registros.append([h, r[i]])
                            l = len(max([str(c) for c in r], key=len))
                            if maxlen < l:
                                maxlen = l

                    header_row = ["Campo", "Valor"]

                tablestr = tabulate(
                    tabular_data        = registros,
                    headers             = [] if args.outputtype == "csv" else header_row,
                    tablefmt            = args.outputtype,
                    stralign            = None if args.outputtype == "csv" else "left",
                    numalign            = None if args.outputtype == "csv" else "rigth"
                )

                if args.outputfile:
                    data_file = os.path.join(args.outputpath, args.outputfile)
                    with open(data_file, "w") as f:
                        f.write(tablestr)

                    log.info("Data saved: {0}".format(data_file))
                else:
                     print(tablestr)


                log.info("Found {0} items in {1}".format(n, elapsed_time))
            else:
                log.error("Data not found in {0}".format(elapsed_time))
        else:
            log.info("Model: {} not implemented".format(data))

    else:
        log.error("model {0} does not exist".format(args.data))
        cmdparser.print_help()

if __name__ == "__main__":

    main()
