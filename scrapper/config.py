from configparser import ConfigParser
import ast

class Config:

    DEF_CFG = {
        "progress_bar_ticks": 5
        }

    def __init__(self, file=None, override=None):

        self.file = file
        self.config = ConfigParser()
        self.__dict__.update(self.DEF_CFG)
        if self.file:
            self._load()

    def set_file(self, file):

        self.file = file
        if self.file:
            self._load()

    def _load(self):

        self.config.read(self.file)

        self.progress_bar_ticks = int(self.config.get("GLOBAL", "progress_bar_ticks"))

    def __str(self):
        return str(self.__dict__)