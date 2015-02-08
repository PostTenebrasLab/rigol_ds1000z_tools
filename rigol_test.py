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

scope = rigol_ds1000z.DS1000z(DEVICE)               # new scope
pl = []

scope.channel[1].set_display(1)                     # turn channel 2 on
scope.channel[1].update_state()

for ch in scope.channel:
    print("Channel "+ch.get_channel_nb()+" "+ch.get_display())
    print("Volt state "+ch.get_voltstate().__str__())
    print("Volt offset "+ch.get_voltoffset().__str__())
    print("Time scale "+ch.get_timescale().__str__())
    print("Time offset "+ch.get_timeoffset().__str__()+"\n")

scope.acquire([1, 2])                              # acquire channel 1 and 2
pl.append(scope.measures[0][1].plot(plot=False))   # keep the plot without plotting it
scope.measures[0][0].save_plot("./pics/test.png")  # save measure 1 channel 1
print(scope.measures[0][0].data.__len__())         # number of points measured

scope.measures[0][0].plot()                        # measure 1 channel 1
scope.measures[0][1].plot()                        # measure 1 channel 2
