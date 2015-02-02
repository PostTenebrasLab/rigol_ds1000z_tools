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


import rigol_ds1000z

DEVICE="/dev/usbtmc0"

ds1074 = rigol_ds1000z.RigolScope(DEVICE)
# ds1074.acquire(channel='1')
ds1074.acquire(channel='1', filename='pics/sin_output-02')#, plot=False)

