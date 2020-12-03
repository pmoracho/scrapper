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
    import cli_options
    import codecs
    import re
    import os
    import logging
    import tempfile
    from urllib.parse import urlparse
    from cotizaciones_bcu import cotizaciones_bcu
    from configparser import ConfigParser
    from tabulate import tabulate
    from tools import make_wide
    from drivers import get_chrome_driver
    from globals import __appname__
    from globals import __appdesc__
    from globals import __copyright__
    from globals import __version__

except ImportError as err:
    modulename = err.args[0].partition("'")[-1].rpartition("'")[0]
    print(_("No fue posible importar el modulo: %s") % modulename)
    sys.exit(-1)

_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.:]+')


def loginfo(msg):
    logging.info(msg.replace("|", " "))

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

    cmdparser = cli_options.init_argparse()

    try:
        args = cmdparser.parse_args()
    except IOError as msg:
        args.error(str(msg))

    if args.outputpath:
        outputpath = args.outputpath
    else:
        outputpath = ''

    logfile = os.path.join(outputpath, 'scrapper.log')
    log_level = getattr(logging, args.loglevel.upper(), None)
    logging.basicConfig(filename=logfile, level=log_level, format='%(asctime)s|%(levelname)s|%(message)s', datefmt='%Y/%m/%d %I:%M:%S', filemode='w')
    logging.info("Starting {0} - {1} (v{2})".format(__appname__, __appdesc__, __version__))

    # determine if application is a script file or frozen exe
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    elif __file__:
        application_path = os.path.dirname(__file__)

    cfgfile = os.path.join(application_path, 'scrapper.cfg')

    loginfo("Loading config: {}".format(cfgfile))
    config = ConfigParser()
    try:
        config.read_file(codecs.open(cfgfile, "r", "utf8"))
    except FileNotFoundError:
        errormsg = "No existe el archivo de configuración ({0})".format(cfgfile)
        print(errormsg)
        logging.error(errormsg)
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

    if args.data:

        datas = [p for p in available_data if p[0] == args.data or args.data == "all"]
        workpath = tempfile.mkdtemp()
        driver = get_chrome_driver(download_folder=workpath, show=args.show_browser)
        for p, n in datas:

            loginfo("Data: {}".format(p))

            # pf = ProcessFlag(p, outputpath)

            section        = "data:" + p
            function_name  = config[section]["function"]
            loginfo("call: {}".format(function_name))
            if function_name in globals():
                function = globals()[function_name]
                datos = function(driver=driver,
                                 parametros=config[section],
                                 tmpdir=workpath)
                tablestr = tabulate(
                                tabular_data        = datos[1:],
                                headers             = datos[0],
                                tablefmt            = args.output_format,
                                stralign            = "left",
                                numalign            = "rigth"
                    )
                print(tablestr)

    else:
        cmdparser.print_help()

if __name__ == "__main__":

    main()
