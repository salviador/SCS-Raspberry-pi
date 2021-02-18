import asyncio
import time
import janus

import sys
sys.path.append('/home/pi/SCS/WEB')
import webapp

#pip3 install janus


loop = asyncio.get_event_loop()


async def taskGetWebserverNew2(jqueqe):
	i = 5
	while(True):
		i = i + 1
		await jqueqe.put(i)
		print(f'{time.ctime()} *taskGetWebserverNew2* ')
		await asyncio.sleep(5)



async def taskGetWebserverNew(jqueqe):
	while(True):
		v = await jqueqe.get()
		print(f'{time.ctime()} *taskGetWebserverNew* ' f'{v}')


async def task1f(jqueqe):
	print(f'{time.ctime()} ENTER TASK1!')
	await asyncio.sleep(12)
	print(f'{time.ctime()} EXTI TASK1!')
	await jqueqe.put(1)


async def task2f(jqueqe):
	await asyncio.sleep(3)
	print(f'{time.ctime()} ENTER TASK2!')
	await asyncio.sleep(3)
	print(f'{time.ctime()} EXTI TASK12')
	await asyncio.sleep(1)
	a = await jqueqe.get()
	print(f'{time.ctime()} EXTI TASK22 ' f'{a}')


async def start_tornado(jqueqe):
	print(f'{time.ctime()} ENTER WEB SERVER')

	app = webapp.make_app()
	app.listen(80)

	webapp.rec_queque(jqueqe)
   	#tornado.ioloop.IOLoop.current().add_callback(display_date)
	#webapp.tornado.ioloop.IOLoop.current().start()
	#webapp.tornado.platform.asyncio.AsyncIOMainLoop().install()

	webapp.tornado.platform.asyncio.AsyncIOMainLoop().install()
	print(f'{time.ctime()} EXIT WEB SERVER')


async def main():
	mjqueqe = janus.Queue()
	queqe_refresh_database = janus.Queue()

	tasks = []
	"""
	tasks.append(asyncio.ensure_future(task1f(mjqueqe.async_q)))
	tasks.append(asyncio.ensure_future(task2f(mjqueqe.async_q)))
	tasks.append(asyncio.ensure_future(start_tornado(queqe_refresh_database.async_q)))
	tasks.append(asyncio.ensure_future(taskGetWebserverNew(queqe_refresh_database.async_q)))
	tasks.append(asyncio.ensure_future(taskGetWebserverNew2(queqe_refresh_database.async_q)))
	"""
	tasks.append(task1f(mjqueqe.async_q))
	tasks.append(task2f(mjqueqe.async_q))
	tasks.append(start_tornado(queqe_refresh_database.async_q))
	tasks.append(asyncio.create_task(taskGetWebserverNew(queqe_refresh_database.async_q)))
	tasks.append(asyncio.create_task(taskGetWebserverNew2(queqe_refresh_database.async_q)))



	asyncio.gather(*tasks)





loop.create_task(main())
loop.run_forever()
loop.close()


