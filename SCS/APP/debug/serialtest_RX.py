import asyncio
from asyncio.events import get_child_watcher
import time
import janus
from gpiozero import LED
from asyncserial import Serial


import sys
sys.path.append('../')

import SCS





enable_opto = LED(12)
enable_opto.on()



loop = asyncio.get_event_loop()

lock_uartTX = asyncio.Lock()

ser = Serial(loop,
        port='/dev/serial0', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
        baudrate = 9600
)

shield = SCS.SCSshield()
shield.SetUART(ser)



"""
Riceve Gli stati AGGIORNATI dei device dal BUS SCS
"""
async def deviceReceiver_from_SCSbus(jqueqe):
	while True:
		trama = await jqueqe.get()
		s=""
		for _ in trama:
			h = '0x' + _.hex()
			s= s + h + ' '
		print(s)
		await asyncio.sleep(0)



async def main():
	mjqueqe = janus.Queue()

	queue_UartRx = janus.Queue()
	shield.Rec_QuequeUartRx(queue_UartRx.async_q)

	queue_rx_trama_data_found = janus.Queue()



	tasks = []
	tasks.append(loop.create_task( shield.uart_rx(queue_rx_trama_data_found.async_q)           ))
	tasks.append(loop.create_task( deviceReceiver_from_SCSbus(queue_rx_trama_data_found.async_q)           ))


	asyncio.gather(*tasks)









loop.create_task(main())
loop.run_forever()
loop.close()

ser.close()
