# -*- coding: utf-8 -*-
"""
Created on Sat Mar 12 22:27:01 2016

@author: zhenhaiyu
"""
import time, os

from watchdog.events import FileSystemEventHandler
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer
from firebase import firebase

firebase = firebase.FirebaseApplication('https://hackalexa.firebaseio.com', None)
endpoint = '/face/'
key = 'numOfVisitors'
pwd = os.getcwd()
video_path = os.path.join(pwd,'videos')
    
def count_file_num(path, ext):
    count = 0
    for file in os.listdir(path):
         if file.endswith(ext):
             count = count + 1
    return count
      
class MyHandler(PatternMatchingEventHandler):
    patterns = ["*.avi"]

    def process(self, event):
        """
        event.event_type 
            'modified' | 'created' | 'moved' | 'deleted'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
        """
        # the file will be processed there
        print event.src_path, event.event_type
        firebase.put('https://hackalexa.firebaseio.com'+endpoint, key, count_file_num(video_path, '.avi'))

#    def on_modified(self, event):
#        self.process(event)

    def on_created(self, event):
        self.process(event)

# ref: http://brunorocha.org/python/watching-a-directory-for-file-changes-with-python.html
if __name__ == '__main__':
    observer = Observer()
    observer.schedule(MyHandler(), path=video_path)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()