from parser import Parser
import queue
import time
import math
import os
import socket
from gui.client import Client
from gui.guilistener import GuiListener
from coffe_machine import PiHatListener
from config import DRINK_IDS
from config import DRINK_UUIDS

if __name__ == "__main__":
    start_time = 0

    dataQueue = queue.PriorityQueue()
    listener = GuiListener(port = 65448, dataQueue = dataQueue)
    listener.setDaemon(True)
    listener.start()

    while True:
        try:
            c = Client('127.0.0.1', 65449)
            break
        except:
            pass
        print('Connecting')
        time.sleep(1)


    parser = Parser(dataQueue = dataQueue)
    parser.setDaemon(True)
    parser.start()


    ph1 = PiHatListener(dataQueue = dataQueue)
    ph1.setDaemon(True)
    ph1.start()
    ph1.subscribeToVMC()

    waiting_transaction = False
    current_address = 2020202
    
    while True:
        msg = dataQueue.get().data

        if 'subscribed' in msg.keys():
            if msg['subscribed'] == True:
                c.sendMessage('mainScreen')
                ph1.subscribed = True


        if 'UUID' in msg.keys() and parser.empty == False:
            choice = None
            for k,v in DRINK_UUIDS.items():
                tmp = v.replace('-', '').upper()
                print(tmp, msg['UUID']['uuid'])
                if tmp == msg['UUID']['uuid'].replace(' ', ''):
                    choice = k
            ph1.startVending()
            time.sleep(1)
            ph1.selectBeverage(choice)

        
        if 'gui' in msg.keys():
            if msg['gui'] == 'startVend':
                c.sendMessage('syncScreen')

        if 'id' in msg.keys():
            choice = None
            for k, v in DRINK_IDS.items():
                print(v, msg['id'])
                if k == msg['id']:
                    choice = k
                    amount = v
            print(choice)
            current_address = str(current_address)
            c.sendMessage('paymentScreen-' + current_address + '-' + str(amount) + '-' + choice)
            start_time = time.time()
            waiting_transaction = True

        if 'paid' in msg.keys():
            if msg['paid'] == True: 
                c.sendMessage('finalScreen')
                ph1.subscribeToVMC()
                time.sleep(3)
                waiting_transaction = False
                start_time = 0
                parser.empty = True

        time.sleep(1)
