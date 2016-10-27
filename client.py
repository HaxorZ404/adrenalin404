# required modules
import sys
import socket
import select
import hashlib
import pickle

if (len(sys.argv) < 5):
    print('[usage] python client.py <hostname> <port> <username> <password>')
    sys.exit()

HOST = str(sys.argv[1])
PORT = int(sys.argv[2])
USERNAME = str(sys.argv[3])
PASSWORD = sys.argv[4].encode()
lock = True
database = {}


password = hashlib.sha1(PASSWORD).hexdigest()

with open('database.pickle', 'rb') as file:
    while lock:
        try:
            loaded = pickle.load(file)
            try:
                if password == loaded[USERNAME]:
                    print('Authentification completed \n loading...')
                    lock = False
            except KeyError:
                database.update(loaded)

        except EOFError:
            break
            sys.exit()


class Client():
    def __init__(self):
        self.host = HOST
        self.port = PORT
        self.run = True
        self.buff = 1024
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(2)

    def prompt(self):
        sys.stdout.write('<you> ')
        sys.stdout.flush()

    def main(self):
        try:
            self.sock.connect((self.host, self.port))
        except:
            print('Unable to connect to the remote host: {0}'.format(self.host))
            sys.exit()

        print('connected to the remote host. Start sending messages')
        self.prompt()

        while 1:
            rlist = [sys.stdin, self.sock]

            read_list, write_list, error_list = select.select(rlist, [], [])

            for sock in read_list:

                if sock == self.sock:
                    data = self.sock.recv(self.buff).decode()
                    if not data:
                        print('\nDisconnected from chat server')
                        sys.exit()
                    if data:
                        sys.stdout.write(data)
                        self.prompt()
                else:
                    data = sys.stdin.readline()
                    data =  '[' + USERNAME + '] '+ data
                    self.sock.send(data.encode())
                    self.prompt()

client = Client()
client.main()
