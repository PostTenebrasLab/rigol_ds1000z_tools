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
        os.write(int(self.f), command.encode())

    def get(self, command, length=4096):
        """ Read a command from device """
        self.write(command)
        return os.read(int(self.f), length).decode()

    def read(self, length=4096):
        """ Read a command from device """
        return os.read(int(self.f), length)


class Channel:

    PROBE_RATIO = 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50, 100, 200, 500, 1000
    BUFFER = 20

    def __init__(self, channel, cmd, probe_ratio=PROBE_RATIO[9]):
        self.channel = channel.__str__()
        self.cmd = cmd
        self.display = self.get_display()
        self.probe_ratio = probe_ratio
        if probe_ratio is not self.PROBE_RATIO[9]:
            self.set_probe_ratio(probe_ratio)

        self.voltscale = self.get_voltstate()
        self.voltoffset = self.get_voltoffset()
        self.timescale = self.get_timescale()
        self.timeoffset = self.get_timeoffset()

    def update_state(self):
        """ update all field from the actual scope state

        """
        self.display = self.get_display()
        self.probe_ratio = self.get_probe_ration()
        self.voltscale = self.get_voltstate()
        self.voltoffset = self.get_voltoffset()
        self.timescale = self.get_timescale()
        self.timeoffset = self.get_timeoffset()

    def restore_state(self):
        """ put the scope in this saved state

        """
        # self.set_display(self.display)
        self.set_voltscale(self.voltscale)
        self.set_voltoffset(self.voltoffset)
        self.set_timescale(self.timescale)
        self.set_timeoffset(self.timeoffset)

    def get_display(self):
        """ Is the channel displayed  True/False

        :return: boolean (channel ON/OFF)
        """
        return self.cmd.get(":CHAN"+self.channel+":DISPlay?", self.BUFFER)

    def set_display(self, state):
        if state:
            self.cmd.write(":CHAN"+self.channel+":DISPlay ON")
            print(self.cmd.get(":CHAN"+self.channel+":DISPlay?", self.BUFFER).__str__())
        else:
            self.cmd.write(":CHAN"+self.channel+":DISPlay OFF")
            print(self.cmd.get(":CHAN"+self.channel+":DISPlay?", self.BUFFER).__str__())

    def get_channel_nb(self):
        return self.channel

    def get_voltstate(self):
        return float(self.cmd.get(":CHAN"+self.channel+":SCAL?", self.BUFFER))  # Get the voltage scale

    def set_voltscale(self, scale):
        self.cmd.write(":CHAN"+self.channel+":SCAL "+scale.__str__())

    def get_probe_ration(self):
        return float(self.cmd.get(":CHAN"+self.channel+":PROBe?", self.BUFFER))

    def set_probe_ratio(self, value):
        self.cmd.write(":CHAN"+self.channel+":PROBe "+value.__str__())

    def get_voltoffset(self):
        return float(self.cmd.get(":CHAN"+self.channel+":OFFS?", self.BUFFER)) # And the voltage offset

    def set_voltoffset(self, value):
        self.cmd.write(":CHAN"+self.channel+":OFFS "+value.__str__())

    def get_timescale(self):
        return float(self.cmd.get(":TIMebase:SCALe?", self.BUFFER))     # Get the timescale

    def set_timescale(self, value):
        self.cmd.write(":TIMebase:SCALe "+value.__str__())

    def get_timeoffset(self):
        return float(self.cmd.get(":TIM:OFFS?", self.BUFFER))    # Get the timescale offset

    def set_timeoffset(self, value):
        self.cmd.write(":TIM:OFFS "+value.__str__())


class Acquisition:
    """ acquire a plot from oscilloscope

        :param channel: channel number
        :param plot: display the plot True/False
        :param filename: save image as
    """

    def __init__(self, channel, cmd):
        self.cmd = cmd
        self.title = "Channel "
        self.channel = Channel(channel, self.cmd)
        self.channel.update_state()
        self.unit = ["S", "mS", "uS", "nS"]
        self.data = []
        self.time = []
        self.rate = self.cmd.get(":ACQuire:SRATe?", 20)

    def get_data(self):
        tmp_state = Channel(self.channel.get_channel_nb(), self.cmd)  # save actual state
        self.channel.restore_state()
        self.cmd.write(":STOP")
        print(self.rate.__str__())
        self.rate = self.cmd.get(":ACQuire:SRATe?", 20)
        self.cmd.write(":WAVeform:SOURce CHAN"+self.channel.get_channel_nb())
        self.cmd.write(":WAVeform:MODE NORM")
        self.cmd.write(":WAVeform:FORMat ASCII")
        # self.cmd.write(":RUN")
        self.cmd.write(":KEY:FORC")
        self.channel.update_state()
        raw = self.cmd.get(":WAV:DATA? CHAN"+self.channel.get_channel_nb().__str__(), 119890)
        data = raw.rsplit(",")
        self.data = list(map(lambda x: float(x), data[1:]))
        time = [(x-self.data.__len__()/2)*self.channel.get_timescale()*12/1000 for x in range(0, self.data.__len__())]
        self.time = [x+self.channel.get_timeoffset() for x in time]  # correct the time offset

        while self.channel.get_timescale() <= .1:
            self.channel.set_timescale(float(self.channel.get_timescale())*1000)
            self.time = [x*1000 for x in time]    # correct plot axis
            self.unit.pop(0)                      # units might be the next one

        tmp_state.restore_state()                 # restore previous state

    def plot(self, plot=True):
        """ pretty print data (plot)

        """
        p = pyplot
        p.plot(self.time, self.data)
        p.title(self.title+self.channel.get_channel_nb())
        p.ylim((-4*self.channel.get_voltstate())-self.channel.get_voltoffset(),(4*self.channel.get_voltstate())-self.channel.get_voltoffset())
        p.ylabel("Voltage "+self.channel.get_voltstate().__str__()+" (V)")
        p.xlabel("Time (" + self.unit[0] + ")")
        p.xlim(self.time[0], self.time[-1])
        if plot:
            pyplot.show()
        return p

    def save_plot(self, filename):
        """ save the plot in a file

        :param filename:
        """
        self.plot(plot=False)
        try:
            pyplot.savefig(filename.__str__())
        except FileNotFoundError as e:
            os.write(sys.stderr, e)


class DS1000z:
    """ Class to control a Rigol DS1000 series oscilloscope

    """
    nb_of_channel = range(1, 5)     # those scopes have 4 channel

    def __init__(self, device):
        """ constructor

        :param device: device (/dev/usbtcmX)
        """
        self.cmd = RigolCmd(device)
        self.name = self.cmd.get_name()
        print(self.name+" initialized")
        self.channel = []
        for chan in self.nb_of_channel:       # Create each channel state
            self.channel.append(Channel(chan.__str__(), self.cmd))
            self.channel[-1].update_state()
        self.measures = []              # Acquisitions are placed in this list

    def write(self, command):
        """ send an action command (no return from the scope)

        :param command: command to be send (ex. :CHAN3:DISP OFF)
        """
        self.cmd.write(command)

    def read(self, command, length=4096):
        """ send a cmd to the scope and return it

        :param command: command to be send (ex. :ACQuire:TYPE?)
        :param length: buffer length
        :return: value returned by the scope
        """
        return self.cmd.read(command, length)

    def acquire(self, channel_lst):
        """ append new acquisition(s) to measure list

        :return: id of the measure (self.measure[id])
        """
        lst = []
        for chan in self.nb_of_channel:
            m = Acquisition(chan, self.cmd)
            if chan in channel_lst:

                m.get_data()
            lst.append(m)

        self.measures.append(lst)
        return self.measures.__len__()  # the measure id


class RigolCmd:
    def __init__(self, device):
        self.oscillo = UsbTMC(device)
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

    def get_name(self):
        """ Get device name """
        return self.oscillo.get(self.__ieee488_2['name'], 20)

    def restore_default(self):
        """ Send restore device command """
        self.oscillo.write(self.__ieee488_2['restore_default'])

    def get(self, command, length=4096):
        """ Read a config value from the scope """
        return self.oscillo.get(command, length)

    def write(self, command):
        """ Send an arbitrary command directly to the scope """
        self.oscillo.write(command)

    def read(self, command, length=4096):
        """ Read directly from the scope """
        return self.oscillo.read(command, length)