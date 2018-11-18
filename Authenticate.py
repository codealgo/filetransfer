import time


# import google libraries
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from Queue import Queue
from threading import Thread

#import watchdog libraries
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class Authentication:
    def authenticate(self):
        print "calling Authentication constructor"
        self.g_auth = GoogleAuth()
        self.g_auth.LocalWebserverAuth()
        return (GoogleDrive(self.g_auth))
    
class Watcher:
    def __init__(self):
        self.observer = Observer()
        
    def register(self, gdrive):
        fhandler = Handler(gdrive)
        self.observer.schedule(fhandler, "C:/Users/test", recursive=True)
        self.observer.start()
        try:
            while 1:
                time.sleep(1)
        except:
            self.observer.stop()
            
        self.observer.join()
        
        
        
class Handler(FileSystemEventHandler):
    def __init__(self,gdrive):
        self.filequeue = FileQueue(gdrive=gdrive)
    
    def on_any_event(self, event):
        if event.event_type == 'created':
            self.filequeue.insertqueue(event.src_path)

class FileQueue:
    def __init__(self,gdrive):
        self.gdrive = gdrive
        self.fqueue = Queue()
        
        #create a worker thread
        self.worker = Thread(target=self.uploadfile)
        self.worker.setDaemon(True)
        self.worker.start()
            
    def insertqueue(self,fpath):
        self.fqueue.put(fpath)
        
        
    def uploadfile(self):
        while True:
            tfile = self.gdrive.CreateFile()
            tfile.SetContentFile(self.fqueue.get())
            tfile.Upload()
            self.fqueue.task_done()
        
        self.fqueue.join()       
            
           
