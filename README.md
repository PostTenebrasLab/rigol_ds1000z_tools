# rigol_ds1000z_tools #

Simple script to acquire data from a Rigol DS1000z oscilloscope using Python

by now, juste a script and a few class to retrive data from rigol scope.

script only read data from the scope. So setup your signal and retrive it with this script.


![samples output...](./pics/sin_output-01.png)



## DS1000z class##

can be derived in particulare scope but contain methods and attributs related
to this scope family.

### attributs ###

    * list of channels
    * scope name
    
### methods ###

    * direct read
    * direct write
    * acquire
   
## Acquire ##
    