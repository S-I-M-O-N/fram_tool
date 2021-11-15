# fram_tool
Tool for programming a FRAM like FM18W08 with an Arduino Mega, for retrocomputing or whatever. I used it to test FRAM for replacing SRAM on Gameboy cartridges.\
Python 3 and pyserial are needed for uploading data to the FRAM. The tool allows chip kilobyte sizes in chunks of power 2 i.e. 1kB, 2kB, 4kB, etc. up to a maximum of 1024kB (1MB).
## Usage:
The script allows reading and writing to the FRAM.
To erase the memory you can program the blank.sav file.
For programming you need to connect the pins of the FRAM according to the arduino sketch fram_tool.ino.
The only additional part is a 10k Ohm pull-up resistor between VDD and /CE pin of the FRAM. On the FM18W08-SG these are pin 20 and 28.
To easily connect and remove the chip itself I used a 28 pin SOIC adapter.
## Project
The project is hosted on https://github.com/S-I-M-O-N/fram_tool 

This project is a fork from https://github.com/robsoncouto/eprom by Robson Couto.
