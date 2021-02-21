import asyncio
from asyncio.events import get_child_watcher
import time
import os
import janus
from gpiozero import LED
import subprocess

import SCS
import mqtt
from asyncserial import Serial

import databaseAttuatori
import mqtt

import nodered

import sys
import importlib.machinery
#sys.path.append('/home/pi/SCS/WEB')
#import webapp


dir_path = os.path.dirname(os.path.realpath(__file__))
dir_path_weblist = dir_path.split('/')
s = ''
for i, _ in enumerate(dir_path_weblist):
    if((len(dir_path_weblist)-1) != i):
        s = s + _ + '/'
dir_path_web = s + 'WEB/'

webapp = importlib.machinery.SourceFileLoader('webapp', dir_path_web + 'webapp.py').load_module()

#pip3 install janus
#pip3 install asyncserial
#pip3 install asyncio-mqtt

#ADD MOSQUITTO MQTT WEBSOCKET ENABLE
#https://stackoverflow.com/questions/35338222/mosquitto-err-connection-refused-with-paho-client




enable_opto = LED(12)
enable_opto.on()


dbm = databaseAttuatori.configurazione_database()


loop = asyncio.get_event_loop()

lock_uartTX = asyncio.Lock()

lock_refresh_Database = asyncio.Lock()




ser = Serial(loop,
        port='/dev/serial0', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
        baudrate = 9600
)

shield = SCS.SCSshield()
shield.SetUART(ser)
scsmqtt = mqtt.SCSMQTT()






async def Node_Red_flow(jqueqe):
	#print("START -> Node_Red_flow")
	while(True):
		#print("WAIT -> Node_Red_flow")
		v = await jqueqe.get()
		n = nodered.nodered()
		n.main()


"""
Legge il database e popola la lista device nella classe SCS.SCSshield
"""
def popula_device():
	shield.clearDevice()
	#print("--- CLEARR------------------")
	allDevice = dbm.RICHIESTA_TUTTI_ATTUATORI()
	#print(allDevice)

	for item in allDevice:
		#print("----------------------")
		#print(item)
		#print("----------------------")

		if(((item['indirizzo_Ambiente']) == '') or ((item['indirizzo_PL']) == '') ):
			return

		#s = item['nome_attuatore']
		#smod = re.sub("\s+", "_", s.strip())
		#smod = s
		if (item['tipo_attuatore'] == "on_off"):
			#print("--- DEVICE ON_FF------------------")
			on_off = SCS.Switch(shield)
			on_off.Set_Address(int(item['indirizzo_Ambiente']), int(item['indirizzo_PL']))
			on_off.Set_Nome_Attuatore(item['nome_attuatore'])
			shield.addDevice(on_off)

		elif (item['tipo_attuatore'] == "serrande_tapparelle"):
			#print("--- DEVICE serrande_tapparelle------------------")
			serranda = SCS.Serranda(shield)
			serranda.Set_Address(int(item['indirizzo_Ambiente']), int(item['indirizzo_PL']))
			serranda.set_Timer(int(item['timer_salita']), int(item['timer_discesa']))
			serranda.Set_Nome_Attuatore(item['nome_attuatore'])
			serranda.register_MQTT_POST(scsmqtt,loop)
			shield.addDevice(serranda)

		elif (item['tipo_attuatore'] == "dimmer"):
			#print("--- DEVICE Dimmer------------------")
			dimmer = SCS.Dimmer(shield)
			dimmer.Set_Address(int(item['indirizzo_Ambiente']), int(item['indirizzo_PL']))
			dimmer.Set_Nome_Attuatore(item['nome_attuatore'])
			shield.addDevice(dimmer)

		elif (item['tipo_attuatore'] == "sensori_temperatura"):
			#print("--- DEVICE sensori_temperatura------------------")
			sensore = SCS.Sensori_Temperatura(shield)
			sensore.Set_Address(int(item['indirizzo_Ambiente']), int(item['indirizzo_PL']))
			sensore.Set_Nome_Attuatore(item['nome_attuatore'])
			shield.addDevice(sensore)
			loop.create_task( sensore.Forza_la_lettura_Temperatura(lock_uartTX) )

		elif (item['tipo_attuatore'] == "termostati"):
			#print("--- DEVICE termostati------------------")
			termostato = SCS.Termostati(shield)
			termostato.Set_obj_SensoreTemp( SCS.Sensori_Temperatura(shield) )
			sensore = termostato.Get_obj_SensoreTemp()

			sensore.Set_Address(int(item['indirizzo_Ambiente']), int(item['indirizzo_PL']))
			sensore.Set_Nome_Attuatore(item['nome_attuatore'])
			shield.addDevice(sensore)

			termostato.Set_Address(int(item['indirizzo_Ambiente']), int(item['indirizzo_PL']))
			termostato.Set_Nome_Attuatore(item['nome_attuatore'])
			shield.addDevice(termostato)
			loop.create_task( sensore.Forza_la_lettura_Temperatura(lock_uartTX) )

		#POPOLARE CON ALTRI TIPI DI DEVICE
		#POPOLARE CON ALTRI TIPI DI DEVICE
		#POPOLARE CON ALTRI TIPI DI DEVICE
		#POPOLARE CON ALTRI TIPI DI DEVICE
		#POPOLARE CON ALTRI TIPI DI DEVICE

"""
A ogni cambiamento della configurazione proveniente dal WEBSERVER 
Aggiorna  il database e popola la lista device nella classe SCS.SCSshield
"""
async def tsk_refresh_database(jqueqe):
	global shield
	while(True):
		try:
			v = await jqueqe.get()
			#print(f'{time.ctime()} *NEED Refresh Database* ' f'{v}')
			#print(type(v))

			#su v ho il vecchio attuatore,
			#cancellare le vecchie sottoscrizioni con publish retain null message
			if(type(v) != int):
				try:
					nomeAtt = v['nome_attuatore']
					tipoAtt = v['tipo_attuatore']
					
					#print("Send Null MQTT retain")

					if(tipoAtt == 'on_off'):
						await scsmqtt.post_to_MQTT_retain_reset("/scsshield/device/" + nomeAtt + "/status")
						await scsmqtt.post_to_MQTT_retain_reset("/scsshield/device/" + nomeAtt + "/switch")
					elif(tipoAtt == 'dimmer'):
						await scsmqtt.post_to_MQTT_retain_reset("/scsshield/device/" + nomeAtt + "/status")
						await scsmqtt.post_to_MQTT_retain_reset("/scsshield/device/" + nomeAtt + "/dimmer")
						await scsmqtt.post_to_MQTT_retain_reset("/scsshield/device/" + nomeAtt + "/status/percentuale")
					elif(tipoAtt == 'serrande_tapparelle'):
						await scsmqtt.post_to_MQTT_retain_reset("/scsshield/device/" + nomeAtt + "/status")
						await scsmqtt.post_to_MQTT_retain_reset("/scsshield/device/" + nomeAtt + "/percentuale")
					elif(tipoAtt == 'sensori_temperatura'):
						await scsmqtt.post_to_MQTT_retain_reset("/scsshield/device/" + nomeAtt + "/request")
						await scsmqtt.post_to_MQTT_retain_reset("/scsshield/device/" + nomeAtt + "/status")
					elif(tipoAtt == 'termostati'):
						await scsmqtt.post_to_MQTT_retain_reset("/scsshield/device/" + nomeAtt + "/status")
						await scsmqtt.post_to_MQTT_retain_reset("/scsshield/device/" + nomeAtt + "/temperatura_termostato_impostata")
						await scsmqtt.post_to_MQTT_retain_reset("/scsshield/device/" + nomeAtt + "/modalita_termostato_impostata")
						await scsmqtt.post_to_MQTT_retain_reset("/scsshield/device/" + nomeAtt + "/set_temp_termostato")
						await scsmqtt.post_to_MQTT_retain_reset("/scsshield/device/" + nomeAtt + "/set_modalita_termostato")
				except KeyError as k:
					pass
			#async with lock_uartTX:        
			popula_device()
		except Exception as e:
			print("2 - ERRRRRRRRRRRRRRRRRRRRR")
			print(e)		

"""
Riceve messaggi da MQTT topic_filter = "/scsshield/device/#"
e invia comandi al BUS SCS

ON_OFF
mosquitto_sub -h localhost -t "/scsshield/device/nome_device/status"
mosquitto_pub -h localhost -t "/scsshield/device/nome_device/switch" -m "1"

DIMEMR
mosquitto_pub -h localhost -t "/scsshield/device/nome_device/dimmer" -m "1"

Sensori_Temperatura
"/scsshield/device/nome_device/request" 

"""
async def mqtt_action(jqueqe):
	while(True):
		try:
			v = await jqueqe.get()
			#print(f'{time.ctime()} *MQTT topic_filter* ' f'{v.topic} '  f'{v.payload} ')
			message = str(v.payload, 'utf-8')

			b = (v.topic).split("/")
			mtopicbase = ('/' + b[1] + '/' + b[2] + '/')
			if( scsmqtt.topic_filter[:-1] in mtopicbase ):
				device_name = b[3]
				devices= shield.getDevices()
				for device in devices:
					ndevice = device.Get_Nome_Attuatore()
					if(ndevice == device_name):
						#TROVATO MATCH nel NOME NEL DATABASE
						#estrapola:
						#Tipo
						#Invia Comando x Tipo dispositivo
						tdevice = device.Get_Type()
						if(tdevice.name == SCS.TYPE_INTERfACCIA.on_off.name):
							action = b[4]
							if(action.lower() == "switch"):
								if((message.lower() == "on") or (message.lower() == "1")):
									cmd1 = loop.create_task( device.On(lock_uartTX) )
									await (cmd1)
								elif((message.lower() == "off") or (message.lower() == "0")):
									cmd1 = loop.create_task( device.Off(lock_uartTX) )
									await (cmd1)
								elif((message.lower().startswith("t")) or (message.lower() == "2")):
									cmd1 = loop.create_task( device.Toggle(lock_uartTX) )
									await (cmd1)
						elif(tdevice.name == SCS.TYPE_INTERfACCIA.dimmer.name):
							action = b[4]
							if(action.lower() == "dimmer"):
								if((message.lower() == "on") or (message.lower() == "1")):
									cmd1 = loop.create_task( device.On(lock_uartTX) )
									await (cmd1)
								elif((message.lower() == "off") or (message.lower() == "0")):
									cmd1 = loop.create_task( device.Off(lock_uartTX) )
									await (cmd1)
								elif((message.lower().startswith("t")) or (message.lower() == "2")):
									cmd1 = loop.create_task( device.Toggle(lock_uartTX) )
									await (cmd1)
								else:
									cmd1 = loop.create_task( device.Set_Dimmer_percent(message, lock_uartTX) )
									await (cmd1)


						elif(tdevice.name == SCS.TYPE_INTERfACCIA.serrande_tapparelle.name):
							action = b[4]
							if(action.lower() == "percentuale"):
								#print("3 --- SERANDA MQTT AZIONE in %: ", message)

								try:
									cmd1 = loop.create_task(device.Azione(int(message), lock_uartTX))
									await (cmd1)
								except Exception as e:
									print("EEEEEEEEEEEERRRRRROTTTTT")
									print(e)

						elif(tdevice.name == SCS.TYPE_INTERfACCIA.sensori_temperatura.name):
							action = b[4]
							if(action.lower() == "request"):
								cmd1 = loop.create_task(device.Forza_la_lettura_Temperatura(lock_uartTX))
								await (cmd1)

						elif(tdevice.name == SCS.TYPE_INTERfACCIA.termostati.name):
							action = b[4]
							if(action.lower() == "set_temp_termostato"):
								cmd1 = loop.create_task(device.set_temp_termostato(float(message), lock_uartTX))
								await (cmd1)
							elif(action.lower() == "set_modalita_termostato"):
								cmd1 = loop.create_task(device.set_modalita_termostato(message, lock_uartTX))
								await (cmd1)


		except Exception as e:
			print("3 - ERRRRRRRRRRRRRRRRRRRRR")
			print(e)




		await asyncio.sleep(0)

"""
Riceve Gli stati AGGIORNATI dei device dal BUS SCS
e li invia a MQTT

Pubblica messaggi da MQTT "/scsshield/device/nome_device/status"

mosquitto_pub -h localhost -t /scsshield/device/Luce Corridoio/switch -m "0" 
mosquitto_sub -h localhost -t "/scsshield/device/Luce Corridoio/status"

#Serrande
"/scsshield/device/Luce Corridoio/percentuale"		#x comando
"/scsshield/device/Luce Corridoio/status"			#x lo stato

#dimmer
"/scsshield/device/Luce Corridoio/dimmer"		#x comando
"/scsshield/device/Luce Corridoio/status"			#x lo stato on/off
"/scsshield/device/Luce Corridoio/status/percentuale"			#x lo stato percentuale

#sensori temperatura
"/scsshield/device/Sensore Temperatura Cucina/status"			#x lo stato get_temp

#termostato
"/scsshield/device/nomeTermostato/status"
"/scsshield/device/nomeTermostato/temperatura_termostato_impostata"		#aggiorna la tempratura di setting termostato
"/scsshield/device/nomeTermostato/modalita_termostato_impostata"
"/scsshield/device/nomeTermostato/set_temp_termostato"
"/scsshield/device/nomeTermostato/set_modalita_termostato"
"""

async def deviceReceiver_from_SCSbus(jqueqe):
	while True:
		trama = await jqueqe.get()

		try:
			#print("uart_rx_deviceReceiver LEN: {}" .format(len(trama)))
			#print("uart_rx_deviceReceiver: {}" .format(trama))

			devices= shield.getDevices()
			for device in devices:
				type = device.Get_Type()
				ndevice = device.Get_Nome_Attuatore()
				addA = device.Get_Address_A()
				addPL = device.Get_Address_PL()

				address = b'\x00'
				address = SCS.bitwise_and_bytes(bytes([addA]), b'\x0F')
				address = SCS.bitwise_shiftleft_bytes(address , b'\x04')
				address = SCS.bitwise_and_bytes(address, b'\xF0')
				address = SCS.bitwise_or_bytes(address, bytes([addPL]) )
				
				#Address MATCH ?
				if(address == trama[2]):
					# SWITCH
					if((len(trama) == 7) and (trama[1] == b'\xB8') and (type.name == SCS.TYPE_INTERfACCIA.on_off.name)):
						statoDevice_in_Bus = int.from_bytes(trama[4], "big")
						device.Set_Stato(statoDevice_in_Bus)
						##Update MQTT
						if(statoDevice_in_Bus == 1):
							await scsmqtt.post_to_MQTT("/scsshield/device/" + ndevice + "/status", "off")
						else:
							await scsmqtt.post_to_MQTT("/scsshield/device/" + ndevice + "/status", "on")
						
					# DIMMER
					elif((len(trama) == 7) and (trama[1] == b'\xB8') and (type.name == SCS.TYPE_INTERfACCIA.dimmer.name)):
						statoDevice_in_Bus = int.from_bytes(trama[4], "big")
						device.Set_Stato(statoDevice_in_Bus)
						dimperc = device.Get_Dimmer_percent()
						##Update MQTT
						if(statoDevice_in_Bus == 1):
							await scsmqtt.post_to_MQTT("/scsshield/device/" + ndevice + "/status", "off")
						elif(statoDevice_in_Bus == 0):
							await scsmqtt.post_to_MQTT("/scsshield/device/" + ndevice + "/status", "on")
						else:
							await scsmqtt.post_to_MQTT("/scsshield/device/" + ndevice + "/status", "on")
							await scsmqtt.post_to_MQTT("/scsshield/device/" + ndevice + "/status/percentuale", dimperc)

					# SERRANDE TAPPARELLE
					elif((len(trama) == 7) and (trama[1] == b'\xB8') and (type.name == SCS.TYPE_INTERfACCIA.serrande_tapparelle.name)):
						statoDevice_in_Bus = int.from_bytes(trama[4], "big")
						device.Set_Stato(statoDevice_in_Bus)
						
						if((trama[1] == b'\xB8') and (trama[3] == b'\x12') and (trama[4] == b'\x0A')):
							#STOP
							device.Ricalcolo_Percent_from_timerelaspe()
							device.stop_timer()

						elif((trama[1] == b'\xB8') and (trama[3] == b'\x12') and (trama[4] == b'\x08')):
							#APRI
							device.RecTimer(1)
							device.start_timer((device.timer_salita_/1000)+2)

						elif((trama[1] == b'\xB8') and (trama[3] == b'\x12') and (trama[4] == b'\x09')):
							#CHIUDI
							device.RecTimer(-1)
							device.start_timer((device.timer_discesa_/1000)+2)

					# sensori Temperature
					elif((len(trama) == 7) and (trama[1] == b'\xB4') and (type.name == SCS.TYPE_INTERfACCIA.sensori_temperatura.name)):
						rawtemp = int.from_bytes(trama[4], "big")
						temp = rawtemp / 10 
						device.Set_Stato(temp)

						await scsmqtt.post_to_MQTT("/scsshield/device/" + ndevice + "/status", temp )

					# campanello
					elif((len(trama) == 7) and (trama[1] == b'\x91') and (trama[3] == b'\x60') and (trama[4] == b'\x08') and (type.name == SCS.TYPE_INTERfACCIA.campanello_porta.name)):
						pass

					# Gruppi
					elif((len(trama) > 7) and (trama[1] == b'\xEC') and (type.name == SCS.TYPE_INTERfACCIA.gruppi.name)):
						pass

					# TERMOSTATO <<Temperatura setting>>
					elif((len(trama) > 7) and (trama[1] == b'\xD2') and (trama[3] == b'\x03') and (trama[4] == b'\x04') and (trama[5] == b'\xC0') and (type.name == SCS.TYPE_INTERfACCIA.termostati.name)):
						rawtemp = int.from_bytes(trama[7], "big")
						if(rawtemp != 0):
							temperature_di_Setting = ((rawtemp - 6) * 0.50) + 3
							device.Set_Temperatura_Termostato(temperature_di_Setting)

							await scsmqtt.post_to_MQTT("/scsshield/device/" + ndevice + "/temperatura_termostato_impostata", temperature_di_Setting )

					# TERMOSTATO <<Temperatura di settaggio>> e <<Modalità freddo o caldo>>
					elif((len(trama) > 7) and (trama[1] == b'\xD2') and (trama[3] == b'\x03') and (trama[4] == b'\x04') and (trama[5] == b'\x12') and (type.name == SCS.TYPE_INTERfACCIA.termostati.name)):
						msb = int.from_bytes(trama[7], "big")
						lsb = int.from_bytes(trama[8], "big")
						tempv  = msb * 256 + lsb
						temp = tempv / 10
						device.Set_Temperatura_Termostato(temp)

						await scsmqtt.post_to_MQTT("/scsshield/device/" + ndevice + "/temperatura_termostato_impostata", temp )

						#Modalità Termostato
						bit1 = SCS.bitwise_and_bytes(trama[6], b'\x0F')

						if((bit1 == b'\x02') or (bit1 == b'\x00')):
							#Inverno
							device.Set_Modalita_Termostato(device.MODALITA.INVERNO)
							await scsmqtt.post_to_MQTT("/scsshield/device/" + ndevice + "/modalita_termostato_impostata", device.MODALITA.INVERNO.name )
						elif((bit1 == b'\x03') or (bit1 == b'\x01')):
							#estate
							device.Set_Modalita_Termostato(device.MODALITA.ESTATE)
							await scsmqtt.post_to_MQTT("/scsshield/device/" + ndevice + "/modalita_termostato_impostata", device.MODALITA.ESTATE.name )
						elif(trama[6] == b'\xFF'):
							#off
							device.Set_Modalita_Termostato(device.MODALITA.OFF)
							await scsmqtt.post_to_MQTT("/scsshield/device/" + ndevice + "/modalita_termostato_impostata", device.MODALITA.OFF.name )

					# TERMOSTATO <<temperature di Setting>>
					elif((len(trama) > 7) and (trama[1] == b'\xD2') and (trama[3] == b'\x03') and (trama[4] == b'\x04') and (trama[5] == b'\x0E') and (type.name == SCS.TYPE_INTERfACCIA.termostati.name)):
						rawtemp = int.from_bytes(trama[7], "big")
						temp = rawtemp / 10 
						device.Set_Temperatura_Termostato(temp)
						await scsmqtt.post_to_MQTT("/scsshield/device/" + ndevice + "/temperatura_termostato_impostata", temp )


			s=""
			for _ in trama:
				h = '0x' + _.hex()
				s= s + h + ' '
			await scsmqtt.post_to_MQTT("/scsshield/debug/bus", s)

			await asyncio.sleep(0)


		except Exception as e:
			print("4 - ERRRRRRRRRRRRRRRRRRRRR")
			print(e)









async def start_tornado(jqueqe, jqueqeNodeRed):
	print(f'{time.ctime()} WEB SERVER start')

	app = webapp.make_app()
	app.listen(80)

	webapp.rec_queque(jqueqe)
	webapp.rec_queque_NODERED(jqueqeNodeRed)
	
   	#tornado.ioloop.IOLoop.current().add_callback(display_date)
	#webapp.tornado.ioloop.IOLoop.current().start()
	#webapp.tornado.platform.asyncio.AsyncIOMainLoop().install()

	webapp.tornado.platform.asyncio.AsyncIOMainLoop().install()
	#print(f'{time.ctime()} EXIT WEB SERVER')


async def main():
	mjqueqe = janus.Queue()
	queqe_refresh_database = janus.Queue()

	queue_refreshdatabase = janus.Queue()
	queue_mqtt_action = janus.Queue()

	queue_node_red_action = janus.Queue()

	queue_UartRx = janus.Queue()
	shield.Rec_QuequeUartRx(queue_UartRx.async_q)

	queue_rx_trama_data_found = janus.Queue()



	tasks = []
	#Tornado START
	tasks.append(asyncio.create_task(start_tornado(queue_refreshdatabase.async_q, queue_node_red_action.async_q )))
	#Refresh Database
	tasks.append(loop.create_task( tsk_refresh_database(queue_refreshdatabase.async_q)           ))
	
	#Test	
	tasks.append(loop.create_task( shield.uart_rx(queue_rx_trama_data_found.async_q)           ))
	tasks.append(loop.create_task( deviceReceiver_from_SCSbus(queue_rx_trama_data_found.async_q)           ))

	tasks.append(asyncio.create_task( scsmqtt.main(queue_mqtt_action.async_q)        ))
	tasks.append(loop.create_task( mqtt_action(queue_mqtt_action.async_q)           ))


	tasks.append(loop.create_task( Node_Red_flow(queue_node_red_action.async_q)           ))



	asyncio.gather(*tasks)





#rimuove TUTTI i RETAIN message in mosquitto
os.popen("sudo systemctl stop mosquitto.service").read()
os.popen("sudo rm /var/lib/mosquitto/mosquitto.db").read()
os.popen("sudo systemctl start mosquitto.service").read()



popula_device()

process = subprocess.Popen(['node-red-start'],
					stdout=subprocess.PIPE, 
					stderr=subprocess.PIPE)

#print(process)


process = subprocess.Popen(['systemctl', 'status nodered.service'],
					stdout=subprocess.PIPE, 
					stderr=subprocess.PIPE)                        

#print(process)
    

loop.create_task(main())
loop.run_forever()
loop.close()

ser.close()
