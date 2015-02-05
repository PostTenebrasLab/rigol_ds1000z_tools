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

    def get(self, command, length=4096):
        """ Read a command from device """
        self.write(command)
        return os.read(self.f, length)

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


class Acquisition:
    """ Class who collect datas and acquisition state from the scope

    """
    def __init__(self, device, channel, mode='NORM', form='ASCII'):
        self.oscillo = UsbTMC(device)
        self.mode = mode
        self.channel = channel.__str__()
        self.title = "Channel "+self.channel
        self.format = form
        self.name = self.oscillo.get_name()
        self.rate = self.oscillo.get(":ACQuire:SRATe?", 20)
        self.mem_depth = self.oscillo.get(":ACQuire:MDEPth?", 20)
        self.voltscale = float(self.oscillo.get(":CHAN"+self.channel+":SCAL?", 20))  # Get the voltage scale
        self.voltoffset = float(self.oscillo.get(":CHAN"+self.channel+":OFFS?", 20)) # And the voltage offset
        self.timescale = float(self.oscillo.get(":TIM:SCAL?", 20))     # Get the timescale
        self.timeoffset = float(self.oscillo.get(":TIM:OFFS?", 20))    # Get the timescale offset


    def refresh_state(self):
        self.name = self.oscillo.get_name()
        self.rate = self.oscillo.get(":ACQuire:SRATe?", 20)
        self.mem_depth = self.oscillo.get(":ACQuire:MDEPth?", 20)
        self.voltscale = float(self.oscillo.get(":CHAN"+self.channel+":SCAL?", 20))  # Get the voltage scale
        self.voltoffset = float(self.oscillo.get(":CHAN"+self.channel+":OFFS?", 20)) # And the voltage offset
        self.timescale = float(self.oscillo.get(":TIM:SCAL?", 20))     # Get the timescale
        self.timeoffset = float(self.oscillo.get(":TIM:OFFS?", 20))    # Get the timescale offset

    def set_mode(self, mode):
        self.mode = mode

    def set_format(self, form):
        self.format = form

    def set_mem_depth(self, mem):
        """ set the memory depth

        When a single channel is on: {AUTO|12000|120000|1200000|12000000|24000000}
        When dual channels are on: {AUTO|6000|60000|600000|6000000|12000000}
        When four channels are on: {AUTO|3000|30000|300000|3000000|6000000}
        Wherein, 24000000, 12000000 and 6000000 are optional.
        :param mem:
        :return:
        """
        self.oscillo.write(":ACQuire:MDEPth "+mem)
        self.mem_depth = self.get_mem_depth()

    def get_mem_depth(self):
        return self.oscillo.get(":ACQuire:MDEPth?", 20)

    def get_datas(self):
        # refresh the actual state (!! state and datas must be synchronised to be relevant !!)
        self.refresh_state()
        # Set the channel of which waveform data will be read.
        self.oscillo.write(":WAVeform:SOURce CHAN"+self.channel)
        # Set the reading mode used by :WAVeform:DATA?
        self.oscillo.write(":WAVeform:MODE "+self.mode)
        if self.mode is "RAW":
            self.oscillo.write(":STOP")
        # Set or query the return format of the waveform data.
        self.oscillo.write(":WAVeform:FORMat "+self.format)
        # header = self.oscillo.read(10).decode()
        # print(header.__str__())
        raw = self.oscillo.get(":WAV:DATA? CHAN"+self.channel, 119890).decode()
        # print(raw.__str__())
        data = raw.rsplit(",")
        header = data[0][6:10]
        print(header.__str__())
        data = list(map(lambda x: float(x), data[1:]))

        unit = ["S", "mS", "uS", "nS"]
        time = [(x-data.__len__()/2)*self.timescale*12/1000 for x in range(0, data.__len__())]
        time = [x+self.timeoffset for x in time]  # correct the time offset
        while self.timescale <= .1:
            self.timescale *= 1000
            time = [x*1000 for x in time]    # correct plot axis
            unit.pop(0)                      # units might be the next one
        # Start data acquisition again, and put the scope back in local mode
        self.oscillo.write(":RUN")
        return data


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
        print(raw.__str__())
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