import threading
import queue
import time
import select
import sys
import socket
from priorityentry.priorityentry import PriorityEntry
class PiHatListener(threading.Thread):
    subscribed = False

    def __init__(self, dataQueue, loop_time = 1.0/60):
        self.functionQueue = queue.Queue()
        self.dataQueue = dataQueue
        self.timeout = loop_time
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect(('127.0.0.1', 65451))
        super(PiHatListener, self).__init__()


    def onThread(self, function, *args, **kwargs):
        self.functionQueue.put((function, args, kwargs))

    def run(self):
        while True:
            try:
                function, args, kwargs = self.functionQueue.get(timeout = self.timeout)
                function(*args, **kwargs)
            except queue.Empty:
                print("check")
                self.idle()

    

    def idle(self):
        data = self.s.recv(1024)
        print(data)
        self.read(data)

    def subscribeToVMC(self):
        self.s.sendall(b'C,1')

    def unsubscribeToVMC(self):
        self.s.sendall(b'C,0')
    
    def startVending(self, amount = 10.0):
        self.s.sendall(str.encode('C,START,' + str(amount)))

    def selectBeverage(self, ids = 'def'):
        self.s.sendall(str.encode('C,SELECT,' + ids))

    def confirmVending(self, amount = 0.5):
        self.s.sendall(str.encode('C,VEND,' + str(amount)))
    
    def declineVending(self):
        self.s.sendall(str.encode('C,VEND,0'))


    def read(self, line):
        if b'ENABLED' == line:
            print(line)
            self.dataQueue.put(PriorityEntry(1, {'subscribed':True}))
        elif b'DISABLED' == line:
            self.dataQueue.put(PriorityEntry(1, {'subscribed':False}))
        elif b'VEND' in line:
            ids = line.decode('utf-8').strip().split(',')[2]
            print(ids + 'ids')
            self.dataQueue.put(PriorityEntry(1, {'id': ids}))
        elif b'PAID' == line:
            self.dataQueue.put(PriorityEntry(1, {'paid': True}))
