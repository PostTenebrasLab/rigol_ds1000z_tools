""" Rigol oscilloscope using Python


    Post Tenebras Lab the geneva(Hackerspace)
"""

__author__ = 'Sebastien Chassot'
__author_email__ = 'sebastien@sinux.net'

__version__ = "1.0.1"
__copyright__ = ""
__maintainer__ = "Sebastien Chassot"
__licence__ = "GPL"
__status__ = ""

import sys
import os
import matplotlib.pyplot as pyplot

class UsbTMC:
    """ Simple implementation of a USBTMC device driver """

    def __init__(self, device):
        self.device = device
        try:
            self.f = os.open(self.device, os.O_RDWR)
        except OSError as err:
            print("Error opening device fd : {0}".format(err), file=sys.stderr)

    def write(self, command):
        """ write a command to device """
        os.write(self.f, command.encode())

    def read(self, length=4096):
        """ Read a command from device """
        return os.read(self.f, length)

    def get_name(self):
        """ Get device name """
        os.write(self.f, b"*IDN?")
        return self.read(300).decode("utf-8")

    def send_reset(self):
        """ Send reset device command """
        os.write(self.f, b"*RST")


class RigolScope:
    """ Class to control a Rigol DS1000 series oscilloscope """

    def __init__(self, device):
        self.oscillo = UsbTMC(device)
        self.name = self.oscillo.get_name()
        print(self.name)

    def write(self, command):
        """ Send an arbitrary command directly to the scope """
        self.oscillo.write(command)

    def read(self, command, lenght=4096):
        """ Read a config value from the scope """
        self.oscillo.write(command)
        return self.oscillo.read(lenght)

    def reset(self):
        """ Reset the instrument """
        self.oscillo.send_reset()

    def acquire(self, channel='1', plot=True, filename=None):
        """ acquire a plot from oscilloscope

        :param channel: channel number
        :param plot: display the plot True/False
        :param filename: save image as
        """
        TITLE="Channel "
        self.write(":STOP")
        rate = self.read(":ACQuire:SRATe?", 20)
        print(rate.__str__())
        # Set or query the channel of which waveform data will be read.
        self.write(":WAVeform:SOURce CHAN"+channel)
        # Set or query the reading mode used by :WAVeform:DATA?
        self.write(":WAVeform:MODE NORM")
        # Set or query the return format of the waveform data.
        self.write(":WAVeform:FORMat ASCII")
        raw = self.read(":WAV:DATA? CHAN"+channel, 119890)
        data = raw.decode().rsplit(",")
        data = list(map(lambda x: float(x), data[1:]))

        # Start data acquisition again, and put the scope back in local mode
        self.write(":RUN")
        self.write(":KEY:FORC")

        voltscale = float(self.read(":CHAN"+channel+":SCAL?", 20))  # Get the voltage scale
        voltoffset = float(self.read(":CHAN"+channel+":OFFS?", 20)) # And the voltage offset
        timescale = float(self.read(":TIM:SCAL?", 20))     # Get the timescale
        timeoffset = float(self.read(":TIM:OFFS?", 20))    # Get the timescale offset

        unit = ["S", "mS", "uS", "nS"]
        time = [(x-data.__len__()/2)*timescale*12/1000 for x in range(0,data.__len__())]
        time = [x+timeoffset for x in time]  # correct the time offset
        while timescale <= .1:
            timescale *= 1000
            time = [x*1000 for x in time]    # correct plot axis
            unit.pop(0)                      # units might be the next one

        # Plot the data
        pyplot.plot(time, data)
        pyplot.title(TITLE+channel)
        pyplot.ylim((-4*voltscale)-voltoffset,(4*voltscale)-voltoffset)
        pyplot.ylabel("Voltage "+voltscale.__str__()+" (V)")
        pyplot.xlabel("Time (" + unit[0] + ")")
        pyplot.xlim(time[0], time[-1])
        if filename:
            pyplot.savefig(filename)
        if plot:
            pyplot.show()