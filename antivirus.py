import time
from watchdog.events import FileSystemEventHandler
import threading
from watchdog.observers import Observer
import psutil

attack_directory='C:\\Users\\Smit Gangurde\\Desktop\\l33t\\NTAL\\Files'

start=time.time()
end=time.time()
class MyWatchDog(FileSystemEventHandler):

	def __init__(self, num_of_files_created, num_of_files_deleted):
		self.num_of_files_created = num_of_files_created
		self.num_of_files_deleted = num_of_files_deleted

	def check_number_of_files_changed(self):
		if self.num_of_files_created <= 1 or self.num_of_files_deleted <= 1:
			self.start = time.time()

		if self.num_of_files_created>10 and self.num_of_files_deleted>10 and self.num_of_files_created+self.num_of_files_deleted >= 20:
			self.end = time.time()
			if(self.end - self.start) < 10:
				print("Virus Detected")
				for proc in psutil.process_iter():
					temp=proc.as_dict()['open_files']
					try:
						for i in temp:
							if attack_directory in i[0]:
								proc.kill()
								print(str(proc.name())+" Virus Eliminated")
								self.num_of_files_created=0
								self.num_of_files_deleted=0
					except:
							continue



	def on_any_event(self,event):
		# self.num_of_files_changed = self.num_of_files_changed + 1
		# if self.num_of_files_changed <= 1:
		# 	self.start=time.time()
		# if self.num_of_files_changed >= 10:
		# 	self.end=time.time()
		# 	if (self.end-self.start) < 5:
		# 		print("Virus bro")
		# 		#PROCNAME = "game_files.exe"
		# 		'''for proc in psutil.process_iter():
		# 			if proc.name()==PROCNAME:
		# 				print(proc.as_dict()['cwd'])
		# 				break'''
		# 		for proc in psutil.process_iter():
		# 			temp=proc.as_dict()['open_files']
		# 			try:
		# 				for i in temp:
		# 					if attack_directory in i[0]:
		# 						proc.kill()
		# 						print("HEHAHAHAHAHAHA I JUST PROTECTED YOUR ASS")
		# 			except:
		# 				continue
		# 			'''if proc.name()==PROCNAME:
		# 				proc.kill()
		# 				print("Virus Eliminated Bro")
		# 				break'''
		# 		self.num_of_files_changed=0
		# #print(self.num_of_files_changed)

		if event.event_type == 'created':
			self.num_of_files_created = self.num_of_files_created+1
			#print("Created "+str(self.num_of_files_created))
			self.check_number_of_files_changed()

		elif event.event_type == 'deleted':
			self.num_of_files_deleted = self.num_of_files_deleted+1
			#print(self.num_of_files_deleted)
			self.check_number_of_files_changed()


class Watcher:

	def __init__(self, DIRECTORY, num_of_files_created, num_of_files_deleted):
		self.observer = Observer()
		self.DIRECTORY = DIRECTORY
		self.num_of_files_created = num_of_files_created
		self.num_of_files_deleted = num_of_files_deleted

	def run(self):
		myWatchDog = MyWatchDog(self.num_of_files_created, self.num_of_files_deleted)
		self.observer.schedule(myWatchDog, self.DIRECTORY, recursive = True)
		self.observer.start()
		try:
			pass
		except:
			self.observer.stop()

		self.observer.join()

if __name__ == '__main__':
	start = time.time()
	num_of_files_created = 0
	num_of_files_deleted = 0
	class MyThread(threading.Thread):
			def __init__(self, DIRECTORY, num_of_files_created, num_of_files_deleted):
				threading.Thread.__init__(self)
				self.DIRECTORY = DIRECTORY
				self.num_of_files_created = num_of_files_created
				self.num_of_files_deleted = num_of_files_deleted

			def run(self):
				w = Watcher(self.DIRECTORY, self.num_of_files_created, self.num_of_files_deleted)
				w.run()

	DIRECTORIES_TO_WATCH = ['C:\\Users\\Smit Gangurde\\Desktop\\l33t\\NTAL\\Files']

	for directory in DIRECTORIES_TO_WATCH:
		w = Watcher(directory, num_of_files_created, num_of_files_deleted)
		w.run()
		#thread = MyThread(directory, num_of_files_changed)
		#thread.start()

	while True:
		pass

