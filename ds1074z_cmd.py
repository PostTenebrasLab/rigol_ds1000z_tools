""" Commands for Rigol DS1074z oscilloscope


    Post Tenebras Lab the geneva(Hackerspace)
"""


__author__ = 'Sebastien Chassot'
__author_email__ = 'sebastien.chassot@etu.hesge.ch'

__version__ = "1.0.1"
__copyright__ = ""
__licence__ = "GPL"
__status__ = ""

import usb_SCPI


class DS1074zCommands:
    """ Implementation of Rigol DS1074z commands

    """
    def __init__(self, device):
        """ Constructor

        :param device: the
        """
        self.oscillo = usb_SCPI.UsbTMC(device)
        self.__acquire_cmd = {
            'average':  ":ACQuire:AVERages",
            'mode': ":ACQuire:MDEPth",
            'type': ":ACQuire:TYPE",
            'sample': ":ACQuire:SRATe"
        }

        self.__ieee488_2 = {
            'clear': "*CLS",
            'name': "*IDN?",
            'restore_default': "*RST",
            'self_test': "*TST?",
            'wait': "*WAI"
        }

    def read(self, command, length=4096):
        """ Read directly from the scope """
        return self.oscillo.read(command, length)

    def write(self, command):
        """ Send an arbitrary command directly to the scope """
        self.oscillo.write(command)

    def get(self, command, length=4096):
        """ Read a config value from the scope """
        return self.oscillo.get(command, length)

    def get_name(self):
        """ Get device name """
        return self.oscillo.get(self.__ieee488_2['name'], 20)

    def restore_default(self):
        """ Send restore device command """
        self.oscillo.write(self.__ieee488_2['restore_default'])





