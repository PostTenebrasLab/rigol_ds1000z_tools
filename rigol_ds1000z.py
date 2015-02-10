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
import ds1074z_cmd

import matplotlib.pyplot as pyplot


class DS1000z:
    """ Class to control a Rigol DS1000 series oscilloscope

    """
    nb_of_channel = range(1, 5)     # those scopes have 4 channel

    def __init__(self, device):
        """ constructor

        :param device: device (/dev/usbtcmX)
        """
        self.cmd = ds1074z_cmd.DS1074zCommands(device)
        self.name = self.cmd.get_name()
        print(self.name+"...scope initialized")
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
            c = Channel(chan, self.cmd)
            m = Acquisition(c)
            if chan in channel_lst:
                m.get_data()
            lst.append(m)
        self.measures.append(lst)

        return self.measures.__len__()  # the measure id

    def get_rate(self):
        return self.cmd.get_rate()


class Channel:

    PROBE_RATIO = 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50, 100, 200, 500, 1000

    def __init__(self, channel, cmd, probe_ratio=PROBE_RATIO[9]):
        self.channel = channel.__str__()
        self.cmd = cmd
        self.display = self.get_display()
        self.probe_ratio = probe_ratio
        if probe_ratio is not self.PROBE_RATIO[9]:
            self.cmd.set_probe_ratio(probe_ratio, channel)

        self.volt_scale = self.get_volt_scale()
        self.volt_offset = self.get_volt_offset()
        self.time_scale = self.get_time_scale()
        self.time_offset = self.get_time_offset()

    def update_state(self):
        """ update all field from the actual scope state

        """
        self.display = self.get_display()
        self.probe_ratio = self.get_probe_ratio()
        self.volt_scale = self.get_volt_scale()
        self.volt_offset = self.get_volt_offset()
        self.time_scale = self.get_time_scale()
        self.time_offset = self.get_time_offset()

    def restore_state(self):
        """ put the scope in this saved state

        """
        self.set_display()
        self.set_probe_ratio(self.probe_ratio)
        self.set_volt_scale(self.volt_scale)
        self.set_volt_offset(self.volt_offset)
        self.set_time_scale(self.time_scale)
        self.set_time_offset(self.time_offset)

    def get_data(self):
        return self.cmd.get_data(self)

    def get_display(self):
        return self.cmd.get_display(self.channel)

    def set_display(self):
        self.cmd.set_display(self.display, self.channel)

    def get_probe_ratio(self):
        return self.cmd.get_probe_ratio(self.channel)

    def set_probe_ratio(self, value):
        self.cmd.set_probe_ratio(value, self.channel)

    def get_volt_scale(self):
        return self.cmd.get_volt_scale(self.channel)

    def set_volt_scale(self, value):
        self.cmd.set_volt_scale(value, self.channel)

    def get_volt_offset(self):
        return self.cmd.get_volt_offset(self.channel)

    def set_volt_offset(self, value):
        self.cmd.set_volt_offset(value, self.channel)

    def get_time_scale(self):
        return self.cmd.get_time_scale()

    def set_time_scale(self, value):
        self.cmd.set_time_scale(value)

    def get_time_offset(self):
        return self.cmd.get_time_offset()

    def set_time_offset(self, value):
        self.cmd.set_time_offset(value)


class Acquisition:
    """ acquire a plot from oscilloscope

        :param channel: channel number
        :param plot: display the plot True/False
        :param filename: save image as
    """

    def __init__(self, channel):
        # self.cmd = cmd
        self.title = "Channel "
        self.channel = channel
        self.channel.update_state()
        self.unit = ["S", "mS", "uS", "nS"]
        self.data = []
        self.time = []

    def get_data(self):
        self.channel.restore_state()
        self.data, self.time, self.unit = self.channel.get_data()

    def plot(self, plot=True):
        """ pretty print data (plot)

        """
        p = pyplot
        p.plot(self.time, self.data)
        p.title(self.title+self.channel.channel)
        p.ylim((-4*self.channel.volt_scale)-self.channel.volt_offset,(4*self.channel.volt_scale)-self.channel.volt_offset)
        p.ylabel("Voltage "+self.channel.volt_scale.__str__()+" (V)")
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

