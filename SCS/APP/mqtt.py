import asyncio
from contextlib import AsyncExitStack, asynccontextmanager
from random import randrange
from asyncio_mqtt import Client, MqttError

import os
from datetime import datetime



class SCSMQTT(object):
    def __init__(self):
        pass

    async def log_messages(self, messages):
        async for message in messages:
            # 🤔 Note that we assume that the message paylod is an
            # UTF8-encoded string (hence the `bytes.decode` call).
            await self.queue.put(message)

            #print(message.payload.decode())

    async def cancel_tasks(self,tasks):
        for task in tasks:
            if task.done():
                continue
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass


    async def advanced_example(self):
        
        self.client = Client("localhost") #, keepalive=60

        # We 💛 context managers. Let's create a stack to help
        # us manage them.
        async with AsyncExitStack() as stack:
            # Keep track of the asyncio tasks that we create, so that
            # we can cancel them on exit

            tasks = set()
            stack.push_async_callback(self.cancel_tasks, tasks)

            # Connect to the MQTT broker
            await stack.enter_async_context(self.client)

            # You can create any number of topic filters
            self.topic_filter = "/scsshield/device/#"

            manager = self.client.filtered_messages(self.topic_filter)
            messages = await stack.enter_async_context(manager)

            task = asyncio.create_task(self.log_messages(messages))
            tasks.add(task)

            manager = self.client.filtered_messages("/scsshield/SendtoBus")
            messages = await stack.enter_async_context(manager)


            task = asyncio.create_task(self.log_messages(messages))
            tasks.add(task)


            # Subscribe to topic(s)
            # 🤔 Note that we subscribe *after* starting the message
            # loggers. Otherwise, we may miss retained messages.
            await self.client.subscribe("/scsshield/SendtoBus")
            await self.client.subscribe(self.topic_filter)

            # Wait for everything to complete (or fail due to, e.g., network
            # errors)
            await asyncio.gather(*tasks)

    async def post_to_topics(self,topic):
        try:
            message = randrange(100)
            print(f'[topic="{topic}"] Publishing message={message}')
            await self.client.publish(topic, message, qos=1)
        except Exception as e:
            print("MQTT ERROR - PUBLISH ")
            print(e)

    def post_to_topicsync(self,topic, message):
        try:
            self.client.publish(topic, message, qos=1)
        except Exception as e:
            print("MQTT ERROR - PUBLISH ")
            print(e)

    async def post_to_MQTT(self, topic, message):
        try:
            await self.client.publish(topic, message, qos=1 , retain = True)
        except Exception as e:
            print("MQTT ERROR - PUBLISH ")
            print(e)

    async def post_to_MQTT_retain_reset(self, topic):
        try:
            await self.client.publish(topic, None, qos=1, retain = True)
        except Exception as e:
            print("MQTT ERROR - PUBLISH ")
            print(e)



    async def main(self, queue):
        # Run the advanced_example indefinitely. Reconnect automatically
        # if the connection is lost.
        self.queue = queue

        reconnect_interval = 3  # [seconds]
        while True:
            try:
                await self.advanced_example()
            except MqttError as error:
                print(f'Error "{error}". Reconnecting in {reconnect_interval} seconds.')
                now = datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                os.popen("sudo echo **MQTT Reconnecting** " + dt_string + " > /dev/kmsg").read()
            finally:
                await asyncio.sleep(reconnect_interval)





if __name__ == "__main__":
    m = SCSMQTT()
    asyncio.run(m.main())
