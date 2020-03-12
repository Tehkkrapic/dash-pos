import socket

class Sender():
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(('127.0.0.1', 65451))

    def sendMessage(self,msg): 
        self.s.sendall(msg.encode('utf-8'))


sender = Sender()

sender.s.listen()
conn, addr = sender.s.accept()
with conn:
    while True:
        data = conn.recv(1024)
        if not data:
            break
        print(data)
        if data == b'C,1':
            conn.sendall(b'ENABLED')
        elif b'SELECT' in data:
            name = data.decode('utf-8').strip().split(',')[2]
            tmp = 'VEND,10,'
            tmp += name
            print(name)
            conn.sendall(tmp.encode('utf-8'))
            x = input()
            conn.sendall(x.encode('utf-8'))
