import asyncio
import os
import signal
import time
from gmqtt import Client as MQTTClient

import os
from datetime import datetime

# gmqtt also compatibility with uvloop  
import uvloop
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

#STOP = asyncio.Event()



"""
pip3 install gmqtt
pip3 install uvloop

"""



#https://github.com/wialon/gmqtt


class SCSMQTT2(object):
    def __init__(self, stop):
        self.STOP = stop





    def on_connect(self, client, flags, rc, properties):
        print(' connected')
        self.client.subscribe('/scsshield/#', qos=0)


    async def on_message(self, client, topic, payload, qos, properties):
        #print('RECV MSG:', payload)
        message = dict()
        message["topic"] = topic
        message["payload"] = payload
        
        await self.queue.put(message)


    def on_disconnect(self, client, packet, exc=None):
        #print('Disconnected')
        pass

    def on_subscribe(self, client, mid, qos, properties):
        #print('SUBSCRIBED')
        pass



    def ask_exit(*args):
        #STOP.set()
        pass




    def post_to_topicsync(self,topic, message):
        try:
            if(self.client.is_connected == True):
                self.client.publish(topic, message, qos=1)
        except Exception as e:
            print("MQTT ERROR - PUBLISH ")
            print(e)

    async def post_to_MQTT(self, topic, message):
        try:
            if(self.client.is_connected == True):
                self.client.publish(topic, message, qos=1 , retain = True)            
        except Exception as e:
            print("MQTT ERROR - PUBLISH {post_to_MQTT} ")
            print(e)

    async def post_to_MQTT_retain_reset(self, topic):
        try:
            if(self.client.is_connected == True):
                self.client.publish(topic, None, qos=1, retain = True)
        except Exception as e:
            print("MQTT ERROR - PUBLISH {post_to_MQTT_retain_reset} ")
            print(e)



    async def main(self, queue):
        # Run the advanced_example indefinitely. Reconnect automatically
        # if the connection is lost.
        self.queue = queue

        try:

                
            self.client = MQTTClient("client-id555")

            self.client.on_connect = self.on_connect
            self.client.on_message = self.on_message
            self.client.on_disconnect = self.on_disconnect
            self.client.on_subscribe = self.on_subscribe

            print("MQTT Connect......... ")

            #self.client.set_auth_credentials(token, None)
            await self.client.connect("localhost",keepalive=65535)

            #client.publish('TEST/TIME', str(time.time()), qos=1)
            #print("MQTT WAIT")

            await self.STOP.wait()

            print("MQTT DISCONNECT")
            await client.disconnect()


        except Exception as e:
            print("MQTT ERROR " , e)
