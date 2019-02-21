from login import *
import threading

def infiniteReceiver():
	while True:
	    event = td_receive()
	    if event:
	        print(event)

threading.Thread(target=infiniteReceiver).start()