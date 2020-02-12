#
from time import time
from urllib.request import urlopen
from threading import Thread
from json import JSONDecoder


def timeit(func):
    def timeit(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        print('Function', func.__name__, 'time:', round((t2 - t1)*1000,1), 'ms')

        return result
    return timeit

class threadTasks:
	def __init__(self):
		self.tasks_dict = {}
		self.results_dict = {}
		self.thread_task_def = {
				    "kwargs": {
				                },
				    "func": None,
				    "result_index": None
				}

	def append_task(self, func, kwargs):
		global thread_task_def
		task_id = max(self.tasks_dict.keys() | [0]) + 1
		
		#Getting task template 
		task_dict = self.thread_task_def.copy()
		
		task_dict["kwargs"] = kwargs
		task_dict["func"] = func
		task_dict["result_index"] = task_id

		#Appending task to tasks_dict
		self.tasks_dict[task_id] = task_dict
		print("added to tasks list - task_id {}".format(task_id))

		return task_id

	#common function for executing tasks
	@timeit
	def thread_executor(self, func, kwargs, result_dict, index):
		try:
			print("executing task id: {} name: {}".format(index, func.__name__))
			result_dict[index] = func(**kwargs)
		except Exception as e:
			print(str(e))
		return True

	#get results for tasks in tasks_dict
	@timeit
	def execute_tasks(self):
		#create a list of threads
		threads = []
		#starting thread per task in tasks_dict 
		for task_id, obj in self.tasks_dict.items():
		    # We start one thread per task
		    process = Thread(target=self.thread_executor, args=[obj['func'], obj['kwargs'], self.results_dict, task_id])
		    process.start()
		    threads.append(process)
		# We now pause execution on the main thread by 'joining' all of our started threads.
		# This ensures that each has finished processing the tasks.
		for process in threads:
		    process.join()

	#Returning thread task result for given id
	def get_results(self, task_id):
		if task_id not in self.tasks_dict:
			print("No tasks registered with id {}".format(task_id))
		elif task_id not in self.results_dict:
			print("No results found for task_id {}".format(task_id))
		else:
			print("Returning results for task_id {}".format(task_id))
			return self.results_dict[task_id]
		return None






