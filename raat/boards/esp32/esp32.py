import logging

from collections import namedtuple

from yapsy.IPlugin import IPlugin

from raat.boards.serial.serial0 import Serial0DueMicro
from raat.boards.generic_board import GenericBoard
from raat.boards.nonvolatile.EEPROM.EEPROM import EEPROM


THIS_PATH = Path(__file__).parent
TEMPLATE = THIS_PATH.joinpath("esp32.template")

class ESP32(
    GenericBoard,
    namedtuple(
        "ESP32",
        [
            "name", "serial", "nonvolatile", "devices", "parameters", "modules",
            "custom_code", "settings", "info", "log_modules", "defines", "arduino_libs",
            "fqbn"
        ]
    )
):

    __slots__ = ()

    @property
    def template(self):
        return TEMPLATE

    @property
    def log_printer(self):
        return "Serial"

    @property
    def progmem(self):
        return ""

    @property
    def required_core(self):
        return "pololu-a-star:avr"


class ESP32Plugin(IPlugin):
    def activate(self):
        pass

    def deactivate(self):
        pass

    def get(self, board, devices, parameters, modules):
        baudrate = board.attrs.get("baudrate", 115200)
        serial = Serial0DueMicro(baudrate)
        nonvolatile = EEPROM()

        return AStar32U4(
            board.name, serial, nonvolatile, devices, parameters, modules,
            board.custom_code, board.settings, board.info, board.log_modules,
            board.defines, board.arduino_libs, fqbn=board.attrs.get("fqbn", "pololu-a-star:avr:a-star32U4")
        )

    def set_log_level(self, level):
        logging.getLogger(__name__).setLevel(level)
