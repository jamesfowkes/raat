import os
import logging

from collections import namedtuple

from yapsy.IPlugin import IPlugin

from adl import template_engine
from adl.boards.serial.serial0 import Serial0
from adl.boards.generic_board import GenericBoard
from adl.boards.uno import UnoBaseType, UnoPlugin

class Duemilanove(UnoBaseType):

    __slots__ = ()

    def __new__(cls, *args, **kwargs):
        if kwargs["fqbn"] is None:
            kwargs["fqbn"] = "arduino:avr:diecimila:cpu=atmega328"
        self = super(UnoBaseType, cls).__new__(cls, *args, **kwargs)
        return self

class DuemilanovePlugin(UnoPlugin):

    def get(self, board, devices, parameters, modules):
        baudrate = board.attrs.get("baudrate", 115200)
        serial = Serial0(baudrate)
        return Duemilanove(board.name, serial, devices, parameters, modules,
            board.custom_code, board.settings, board.info, board.log_modules,
            fqbn=board.attrs.get("fqbn", None)
        )
