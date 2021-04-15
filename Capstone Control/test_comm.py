from getData import Receiver

# Make sure IP and PORT match server side IP and PORT
IP = '192.168.2.2'
PORT = 10001
r = Receiver(IP, PORT)
r.client.connect()

while True:
    r.receive()
    print(r.datalist)
