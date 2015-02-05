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
# ds1074.acquire(channel='1')
# ds1074.acquire(channel='1', filename='pics/sin_output-02')#, plot=False)

scope.channel[1].set_display(0)
scope.channel[1].update_state()

for i in scope.channel:
    print("Channel "+i.get_channel_nb()+" "+i.get_display())
    if i.get_display() == 1:
        print("Volt state "+i.get_voltstate().__str__())
        print("Volt offset "+i.get_voltoffset().__str__())
        print("Time scale "+i.get_timescale().__str__())
        print("Time offset "+i.get_timeoffset().__str__()+"\n")

scope.acquire()
