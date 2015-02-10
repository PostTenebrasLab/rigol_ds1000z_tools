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
    BUFFER = 20

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

    def read(self, length=4096):
        """ Read directly from the scope """
        return self.oscillo.read(length)

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

    def get_display(self, channel):
        """ Is the channel displayed  True/False

        :return: boolean (channel ON/OFF)
        """
        return self.get(":CHAN"+channel+":DISPlay?", self.BUFFER)

    def set_display(self, state, channel):
        if state:
            self.write(":CHAN"+channel+":DISPlay ON")
        else:
            self.write(":CHAN"+channel+":DISPlay OFF")

    def get_volt_scale(self, channel):
        return float(self.get(":CHAN"+channel+":SCAL?", self.BUFFER))  # Get the voltage scale

    def set_volt_scale(self, scale, channel):
        self.write(":CHAN"+channel+":SCAL "+scale.__str__())

    def get_probe_ratio(self, channel):
        return float(self.get(":CHAN"+channel+":PROBe?", self.BUFFER))

    def set_probe_ratio(self, value, channel):
        self.write(":CHAN"+channel+":PROBe "+value.__str__())

    def get_volt_offset(self, channel):
        return float(self.get(":CHAN"+channel+":OFFS?", self.BUFFER)) # And the voltage offset

    def set_volt_offset(self, value, channel):
        self.write(":CHAN"+channel+":OFFS "+value.__str__())

    def get_time_scale(self):
        return float(self.get(":TIMebase:SCALe?", self.BUFFER))     # Get the timescale

    def set_time_scale(self, value):
        self.write(":TIMebase:SCALe "+value.__str__())

    def get_time_offset(self):
        return float(self.get(":TIM:OFFS?", self.BUFFER))    # Get the timescale offset

    def set_time_offset(self, value):
        self.write(":TIM:OFFS "+value.__str__())

    def get_rate(self):
        return float(self.get(":ACQuire:SRATe?", self.BUFFER))

    def get_mem_depth(self):
        return float(self.get(":ACQuire:MDEPth?", self.BUFFER))

    def set_mem_depth(self, value):
        """ Set the memory depth of the oscilloscope

        single channel: {AUTO|12000|120000|1200000|12000000|24000000}
        dual channels: {AUTO|6000|60000|600000|6000000|12000000}
        four channels: {AUTO|3000|30000|300000|3000000|6000000}

        :param value: channel memory depth
        """
        self.write(":ACQuire:MDEPth "+value.__str__())

    def get_data(self, channel):
        unit = ["S", "mS", "uS", "nS"]
        self.write(":STOP")
        self.write(":WAVeform:SOURce CHAN"+channel)
        self.write(":WAVeform:MODE NORM")
        self.write(":WAVeform:FORMat ASCII")
        raw = self.get(":WAV:DATA? CHAN"+channel, 119890)
        data = raw.rsplit(",")
        data = list(map(lambda x: float(x), data[1:]))
        time = [(x-data.__len__()/2)*channel.time_scale*12/1000 for x in range(0, data.__len__())]
        time = [x+channel.time_offset for x in time]  # correct the time offset

        while channel.time_scale <= .1:
            channel.time_scale = float(channel.time_scale)*1000
            time = [x*1000 for x in time]    # correct plot axis
            unit.pop(0)

        return data, time, unit[0]
