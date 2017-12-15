import socket
import time

"""
WIFI class to manage connection with RPI via WIFI connection
"""
class WIFI:
    ip = None
    port = None
    soc = None

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    """
    Start the WIFI connection
    """
    def start(self):
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.soc.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.soc.connect((self.ip, self.port))
        print("Socket Connected!")
    
    """
    Close the WIFI connection
    """
    def end(self):
        self.soc.close()
        self.soc = None
        print("Socket Closed!")

    """
    Send the message via WIFI, reconnect and resend if failed.
    """
    def write(self, data):
        try:
            print("message sent: " + data)
            self.soc.sendall((data).encode())

        except socket.error as e:
            print(e)
            print("Reconnecting to the socket...")
            self.end()
            self.start()
            self.write(data)

    """
    Listen and receive the data from WIFI
    """
    def read(self):
        data = ""
        print("Waiting for incoming data...")
        data = self.soc.recv(1024).decode()
        data = data.strip()

        print("Received data: " + data)
        if len(data) > 0:
            return data
        else:
            return None


