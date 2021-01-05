#!env python
import select

# Set these to control bind host and port for tcp server
BIND_HOST, BIND_PORT = "localhost", 3330

# Set these to control where you are connecting to
HOST, PORT = "localhost", 5902

from socketserver import StreamRequestHandler, TCPServer, ForkingTCPServer
from socket import socket, AF_INET, SOCK_STREAM

class SockHandler(StreamRequestHandler):
    """
    Request Handler for the proxy server.
    Instantiated once time for each connection, and must
    override the handle() method for client communication.
    """

    def handle(self):
        print("handling connection")

        # Create a socket to the localhost server
        sock = socket(AF_INET, SOCK_STREAM)
        # Try to connect to the server and send data
        try:
            sock.connect((HOST, PORT))
            sock.setblocking(False)
            self.connection.setblocking(False)
            print("opened socket " + str(sock))
            # Receive data from the server
            data = None
            received = None
            while 1:
                readable, writeable, exceptional = select.select(
                    [self.rfile, sock], [self.wfile, sock], [], 0)
                for writable_sock in writeable:
                    if writable_sock == sock and data is not None:
                        # print("sock writeable, sending " + str(len(data)))
                        if sock.sendall(data) == 0:
                            return
                        data = None
                    if writable_sock == self.wfile and received is not None:
                        # print("wfile writeable, sending " + str(len(received)))
                        if self.wfile.write(received) == 0:
                            return
                        received = None
                for readable_sock in readable:
                    if readable_sock == self.rfile and data is None:
                        data = self.rfile.read(1024)
                        # print("rfile readable, read " + str(len(data)))
                        if len(data) == 0:
                            return
                    if readable_sock == sock and received is None:
                        received = sock.recv(1024)
                        # print("sock readable, read " + str(len(received)))
                        if len(received) == 0:
                            return

        finally:
            print("closing socket" + str(sock))
            sock.close()

if __name__ == '__main__':
    # Create server and bind to set ip
    myserver = ForkingTCPServer((BIND_HOST, BIND_PORT), SockHandler)

    # activate the server until it is interrupted with ctrl+c
    myserver.serve_forever()