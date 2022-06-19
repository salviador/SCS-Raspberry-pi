#!/usr/bin/env python3
from serial import Serial
import asyncio
import time
import threading
import queue

class SerialHandler(object):
    def __init__(self, port, baudrate=9600):
        self.adict = {}

        ser = Serial(
            port=port,
            baudrate=baudrate
        )
        self.adict['ser'] = ser
        self.adict['rque'] = asyncio.Queue()
        self.adict['loop'] = asyncio.get_event_loop()

        print("Starting handlers..")
        rt = threading.Thread(target=self._read)
        rt.daemon = True
        rt.start()

    async def read(self):
        return await self.adict['rque'].get()

    def _read(self):
        print("TREADER: ONLINE")
        while True:
            line = self.adict['ser'].read(1)
            line += self.adict['ser'].read(self.adict['ser'].in_waiting)
            print("<",line)
            self.adict['loop'].create_task(self.adict['rque'].put(line))

    async def write(self, data):
        line = bytes(bytearray(data))
        print(">",line)
        self.adict['ser'].write(line)

async def main():
    s = SerialHandler('/dev/serial0',9600)
    time.sleep(1)
    print(await s.read())
    while True:
        line = await s.read()
        print(line)

if __name__ == "__main__":
    asyncio.run(main())
