""" communication with scope using Python


    Post Tenebras Lab the geneva(Hackerspace)
"""

__author__ = 'Sebastien Chassot'
__author_email__ = 'sebastien.chassot@etu.hesge.ch'

__version__ = "1.0.1"
__copyright__ = ""
__licence__ = "GPL"
__status__ = ""


import sys
import os


class UsbTMC:
    """ Simple implementation of a USBTMC device driver

    """
    def __init__(self, device):
        """ Constructor

        :param device: device to connect to
        """
        self.device = device
        try:
            self.f = os.open(self.device, os.O_RDWR)
        except OSError as err:
            print("Error opening device fd : {0}".format(err), file=sys.stderr)

    def read(self, length=4096):
        """ Read a command from device """
        return os.read(int(self.f), length)

    def write(self, command):
        """ write a command to device """
        os.write(int(self.f), command.encode())

    def get(self, command, length=4096):
        """ Read a command from device """
        self.write(command)
        return os.read(int(self.f), length).decode()

