#!/usr/bin/env python3
import serial

import time

#https://openenergymonitor.org/forum-archive/node/12311.html
#pip3 uninstall serial
#pip3 uninstall Serial
#pip3 install Pyserial


ser = serial.Serial(
        port='/dev/serial0', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)


while True:
    #ser.write(bytes(b'1\r\n'))
    a = bytearray([45])

    print(ser.read())
    time.sleep(1)