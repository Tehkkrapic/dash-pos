import time
import os

while True:
    os.system('sudo ./ibeacon_scan 2>./tmp.txt &')
    time.sleep(10)
    os.system('sudo pkill -9 ibeacon_scan')
    os.system('sudo pkill -9 hcitools')
    os.system('sudo pkill -9 hcidump')
    os.system('rm tmp.txt')
    time.sleep(2)


