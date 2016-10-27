import socket
import sys
import select

# main variables
_HOST = 'localhost'  # host for the server
_PORT = 4500  # remote port
_BUFFER = 1024  # max buffering for data
_RUNNING = True  # main variable to run the principal loop
_USERS = []  # list of all connected users


class Server:  # socket chat server as an object
    def __init__(self):
        self.host = socket.gethostbyname(_HOST)
        self.port = int(_PORT)
        self.buffer = _BUFFER
        self.run = _RUNNING
        self.users = _USERS
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def broadcast_data(self, sock, data): 
        for sockt in self.users: # to send to all connected users
            if sockt != self.sock and sockt != sock:
                try:
                    sockt.send(data.encode())
                except:
                    sockt.close()
                    self.users.remove(sockt)

    def main(self):
        try:
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind((self.host, self.port))
            self.sock.listen(5)
            self.users.append(self.sock)
        except socket.error:
            print('Unable to connect ot the remote host: {0}'.format(self.host))

        print('Chat server started on port: ' + str(self.port) + '\n')

        while 1:

            read_sockets, write_sockets, in_error = select.select(self.users, [], [])

            for sockp in read_sockets:
                if sockp == self.sock:
                    # new connection
                    sockfd, addr = self.sock.accept()
                    self.users.append(sockfd)
                    print('Client ({0}) connected\n'.format(addr))
                    self.broadcast_data(sockfd, '[{0}] entered the chatroom\n'.format(addr))

            # some incoming message from the client
                else:
                    # data received from the client process it
                    try:
                        data = sockp.recv(self.buffer).decode()
                        if data:
                            print('\r' + '<' + str(sockp.getpeername()) + '> ' + data)
                            self.broadcast_data(sockp, data)
                    except socket.error:
                        self.broadcast_data(sockp, 'Client({0}) is offline\n'.format(addr))
                        print('Client({0}) is offline\n'.format(addr))
                        sockp.close()
                        try:
                            self.users.remove(sockp)
                        except socket.error:
                            print('\r')
                            continue
                        continue
        self.sock.close()

if __name__ == '__main__':
    server = Server()
    server.main()
