import socket
import threading
import queue
from priorityentry.priorityentry import PriorityEntry

def two_comp(val, bits):
        if(val & (1 << (bits - 1))) != 0:
            val = val - (1 << bits)
        return val

class Parser(threading.Thread):
    def __init__(self, dataQueue):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(('127.0.0.1', 65450))
        self.dataQueue = dataQueue
        self.empty = True
        super(Parser,self).__init__()
    
    
       
    def run(self):
        while True:
            self.s.listen()
            conn, addr = self.s.accept()
            with conn:
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    postoji = False
                    data = data.decode('utf-8')
                    uuid = data[60: 107]
                    major = data[108: 114].replace(' ', '')
                    major = int(major, 16)
                    minor = data[114: 119].replace(' ', '')
                    minor = int(minor, 16)
                    tx = data[120: 122]
                    tx = int(tx, 16)
                    tx = two_comp(tx, 8)
                    rssi = data[123:125]
                    rssi = int(rssi, 16)
                    rssi = two_comp(rssi, 8)
                    distance = pow(10, ((tx - rssi) / 20))
                    tmp = {'uuid': uuid,
                            'major': major,
                            'minor': minor,
                            'tx': tx,
                            'rssi': rssi,
                            'distance': distance}
                    print(tmp)
                    if distance < 0.5 and self.empty:
                        self.dataQueue.put(PriorityEntry(1, {'UUID' : tmp}))
                        self.empty = False

