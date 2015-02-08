# rigol_ds1000z_tools #

Simple script to acquire data from a Rigol DS1000z oscilloscope using Python

by now, juste a script and a few class to retrive data from rigol scope.

script only read data from the scope. So setup your signal and retrive it with this script.


![samples output...](./pics/sin_output-01.png)



## DS1000z class##

can be derived in particular scope but contain methods and attributs related
to this scope family.

a scope has 4 channels with settings
a scope has also a measure list (each measure can be plotted, updated, saved,..,)

## RigolCmd ##

it's a link between UsbTMC and scope. The idea behind is to have a by scope cmd class in the future

## Channel ##

this class handel a channel state that can be saved, restored and reapplied. 

It's used to store the 4 channels state but it's also used to restore a measure state 
to update it or backup a particular setting, temporally backup a setting,...

## Acquisition ##

Store a channel setting, datas acquisition, timescale related to the measure.

As the setting is stored, measure state can be restored and measure updated.

It's also possible to save it, plot it, do some action/analyse on datas,...