"""
due to the desire of srchemy,we cant use threadingpool,so we use a controller 
to controll the number of threads that run at the same time,before start a 
thread,we should see how much threads are running on the mechine
"""

import threading
import Queue
#exceptions
class QueueFullerr(Exception):
	"""
	Queue is full,can't put any element into it
	"""
	pass


class ThreadController(object):

	def __init__(self,thread_number):
		self.number = thread_number
		#storepool store all the threads
		#self.sotrepool	= Queue.Queue(maxsize=self.number)
		#runpool store all the running threads
		self.runpool = []


	def append_topool(self,thread_list):
		"""
		thread_list incude a set of objects of threads
		"""
		self.summary = len(thread_list)
		self.storepool = Queue.Queue(maxsize=self.summary)
		for i in thread_list:
				self.storepool.put(i)

	def start(self):
		"""
		"""
		if self.number >= self.summary and not self.storepool.empty():
			th = self.storepool.get()
			th.start()
		else:
			for i in xrange(self.number):
				th = self.storepool.get()
				self.runpool.append(th)
				th.start()
			while(1):
				self._run_clear_job()
				if self.storepool.empty() and len(self.runpool) == 0:
					#all the threads finish
					break
				else:
					continue

	def _run_clear_job(self):
		if threading.activeCount() < self.number + 1:
			for th in self.runpool:
				if not th.is_alive():
					self.runpool.remove(th)
		if not self.storepool.empty() and \
						len(self.runpool) <= self.number:
			th = self.storepool.get()
			self.runpool.append(th)
			th.start()


if __name__ == "__main__":
	import time 
	class Test(threading.Thread):
		def __init__(self):
			super(Test,self).__init__()
		def run(self):
			print threading.currentThread(),"--begin sleep"
			time.sleep(3)
			print threading.currentThread(),"--finish sleep"

	l = []
	for i in range(10):
		temp = Test()
		l.append(temp)

	controller = ThreadController(5)
	controller.append_topool(l)
	controller.start()
	for i in l:
		i.join()

	print "success"









