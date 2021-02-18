import asyncio
import serial_asyncio
import time

#https://openenergymonitor.org/forum-archive/node/12311.html

#pip3 uninstall serial
#pip3 uninstall Serial
#pip3 install Pyserial

#pip3 install pyserial-asyncio
#pip3 install asyncio
#sudo adduser $USER dialout

#https://tinkering.xyz/async-serial/
#https://pyserial-asyncio.readthedocs.io/en/latest/index.html



class Output(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport
        print('port opened', transport)
        transport.serial.rts = False  # You can manipulate Serial object via transport
        transport.write(b'Hello, World!\n')  # Write serial data via transport

    def data_received(self, data):
        print('data received', repr(data))
        #if b'\n' in data:
        #    self.transport.close()

    def connection_lost(self, exc):
        print('port closed')
        self.transport.loop.stop()

    def pause_writing(self):
        print('pause writing')
        print(self.transport.get_write_buffer_size())

    def resume_writing(self):
        print(self.transport.get_write_buffer_size())
        print('resume writing')

loop = asyncio.get_event_loop()
coro = serial_asyncio.create_serial_connection(loop, Output, '/dev/serial0', baudrate=115200)
loop.run_until_complete(coro)
loop.run_forever()
loop.close()


