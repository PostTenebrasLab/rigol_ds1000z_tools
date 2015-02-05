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
        return os.read(self.f, length).decode()

    def read(self, length=4096):
        """ Read a command from device """
        return os.read(self.f, length)


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
        self.data = []
        self.__acquire()

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

    def get_data(self):
        return self.data

    def __acquire(self):
        self.data.clear()
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
        data = self.oscillo.get(":WAV:DATA? CHAN"+self.channel, 119890).decode().split(',')
        # print(raw.__str__())
        # data = raw.rsplit(",")
        # header = data[0][6:10]
        # print(header.__str__())
        self.data = list(map(lambda x: float(x), data[1:]))

        unit = ["S", "mS", "uS", "nS"]
        time = [(x-data.__len__()/2)*self.timescale*12/1000 for x in range(0, data.__len__())]
        time = [x+self.timeoffset for x in time]  # correct the time offset
        while self.timescale <= .1:
            self.timescale *= 1000
            time = [x*1000 for x in time]    # correct plot axis
            unit.pop(0)                      # units might be the next one
        # Start data acquisition again, and put the scope back in local mode
        self.oscillo.write(":RUN")


class Channel:

    PROBE_RATIO = 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50, 100, 200, 500, 1000
    BUFFER = 20

    def __init__(self, channel, cmd, probe_ratio=PROBE_RATIO[9]):
        self.channel = channel
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

    def get_display(self):
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
        self.cmd.write(":CHAN"+self.channel+":SCAL "+scale)

    def get_probe_ration(self):
        return float(self.cmd.get(":CHAN"+self.channel+":PROBe?", self.BUFFER))

    def set_probe_ratio(self, value):
        self.cmd.write(":CHAN"+self.channel+":PROBe "+value)

    def get_voltoffset(self):
        return float(self.cmd.get(":CHAN"+self.channel+":OFFS?", self.BUFFER)) # And the voltage offset

    def set_voltoffset(self, value):
        self.cmd.write(":CHAN"+self.channel+":OFFS "+value)

    def get_timescale(self):
        return float(self.cmd.get(":TIMebase:SCALe?", self.BUFFER))     # Get the timescale

    def set_timescale(self, value):
        self.cmd.write(":TIMebase:SCALe "+value.__str__())

    def get_timeoffset(self):
        return float(self.cmd.get(":TIM:OFFS?", self.BUFFER))    # Get the timescale offset

    def set_timeoffset(self, value):
        return float(self.cmd.write(":TIM:OFFS ", value))


class Acquire:
    """ acquire a plot from oscilloscope

        :param channel: channel number
        :param plot: display the plot True/False
        :param filename: save image as
    """

    def __init__(self, channel, cmd):
        self.cmd =cmd
        self.title = "Channel "
        self.channel = channel
        self.plot = True
        self.data = []
        self.rate = self.cmd.get(":ACQuire:SRATe?", 20)

    def get_data(self):
        self.cmd.write(":STOP")
        print(self.rate.__str__())
        self.rate = self.cmd.get(":ACQuire:SRATe?", 20)
        self.cmd.write(":WAVeform:SOURce CHAN"+self.channel.get_channel_nb())
        self.cmd.write(":WAVeform:MODE NORM")
        self.cmd.write(":WAVeform:FORMat ASCII")
        self.cmd.write(":RUN")
        self.cmd.write(":KEY:FORC")
        self.channel.update_state()
        raw = self.cmd.get(":WAV:DATA? CHAN"+self.channel.get_channel_nb().__str__(), 119890)
        data = raw.rsplit(",")
        self.data = list(map(lambda x: float(x), data[1:]))
        unit = ["S", "mS", "uS", "nS"]
        time = [(x-self.data.__len__()/2)*self.channel.get_timescale()*12/1000 for x in range(0,self.data.__len__())]
        time = [x+self.channel.get_timeoffset() for x in time]  # correct the time offset
        while self.channel.get_timescale() <= .1:
            self.channel.set_timescale(float(self.channel.get_timescale())*1000)
            time = [x*1000 for x in time]    # correct plot axis
            unit.pop(0)                      # units might be the next one

        # Plot the data
        pyplot.plot(time, self.data)
        pyplot.title(self.title+self.channel.get_channel_nb())
        pyplot.ylim((-4*self.channel.get_voltstate())-self.channel.get_voltoffset(),(4*self.channel.get_voltstate())-self.channel.get_voltoffset())
        pyplot.ylabel("Voltage "+self.channel.get_voltstate().__str__()+" (V)")
        pyplot.xlabel("Time (" + unit[0] + ")")
        pyplot.xlim(time[0], time[-1])
        # if filename:
        #     pyplot.savefig(filename)
        # if self.plot:
        #     pyplot.show()


class DS1000z:
    """ Class to control a Rigol DS1000 series oscilloscope """

    probes = {1, 2, 3, 4}

    def __init__(self, device):
        self.cmd = RigolCmd(device)
        self.name = self.cmd.get_name()
        print(self.name+" initialized")
        self.channel = []
        for probe in self.probes:
            self.channel.append(Channel(probe.__str__(), self.cmd))
        for probe in self.channel:
            probe.update_state()

    def write(self, command):
        self.cmd.write(command)

    def read(self, command, lenght=4096):
        return self.cmd.read(command, lenght)

    def acquire(self):
        test = Acquire(self.channel[0], self.cmd)
        # test.get_data('pics/sin_output-03')
        test.get_data()

        # Set or query the channel of which waveform data will be read.
        # Set or query the reading mode used by :WAVeform:DATA?
        # Set or query the return format of the waveform data.
        # Start data acquisition again, and put the scope back in local mode


class RigolCmd:

    def __init__(self, device):
        self.oscillo = UsbTMC(device)
        # self.name = self.get_name()
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

    def __acquire(self, cmd):
        return self.__acquire_cmd[cmd]

    def __ieee488_2(self, cmd):
        return self.__ieee488_2[cmd]

    def get_name(self):
        """ Get device name """
        return self.oscillo.get(self.__ieee488_2['name'], 20)

    def restore_default(self):
        """ Send reset device command """
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