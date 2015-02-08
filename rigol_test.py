#! /usr/bin/python3
# -*- coding: utf-8 -*-

""" Simple script to acquire data from a Rigol oscilloscope


    Post Tenebras Lab the geneva(Hackerspace)
"""

__author__ = 'Sebastien Chassot'
__author_email__ = 'sebastien@sinux.net'

__version__ = "1.0.1"
__copyright__ = ""
__maintainer__ = "Sebastien Chassot"
__licence__ = "GPL"
__status__ = ""


import os
import sys
import time
import rigol_ds1000z

DEVICE = "/dev/usbtmc0"

scope = rigol_ds1000z.DS1000z(DEVICE)
pl = []
# ds1074.acquire(channel='1')
# ds1074.acquire(channel='1', filename='pics/sin_output-02')#, plot=False)

scope.channel[1].set_display(0)
scope.channel[1].update_state()

for ch in scope.channel:
    print("Channel "+ch.get_channel_nb()+" "+ch.get_display())
    print("Volt state "+ch.get_voltstate().__str__())
    print("Volt offset "+ch.get_voltoffset().__str__())
    print("Time scale "+ch.get_timescale().__str__())
    print("Time offset "+ch.get_timeoffset().__str__()+"\n")

scope.acquire()
pl.append(scope.measures[0].plot(plot=False))  # keep the plot
scope.measures[0].save_plot("./pics/test.png")
# print(scope.measures[0].data)

pl[0].show()
